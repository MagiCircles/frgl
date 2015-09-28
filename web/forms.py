from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import BLANK_CHOICE_DASH
from web import models
from django.utils.translation import ugettext_lazy as _, string_concat

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class AddLinkForm(forms.ModelForm):
    class Meta:
        model = models.UserLink
        fields = ('type', 'value', 'relevance')

class UserPreferencesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserPreferencesForm, self).__init__(*args, **kwargs)
        self.fields['favorite_performer'].required = False

    class Meta:
        model = models.UserPreferences
        fields = ('favorite_performer', 'location', 'private', 'description')

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(), label=_('Old Password'))
    new_password = forms.CharField(widget=forms.PasswordInput(), label=_('New Password'))
    new_password2 = forms.CharField(widget=forms.PasswordInput(), label=_('New Password Again'))

    def clean(self):
        if ('new_password' in self.cleaned_data and 'new_password2' in self.cleaned_data
            and self.cleaned_data['new_password'] == self.cleaned_data['new_password2']):
            return self.cleaned_data
        raise forms.ValidationError(_("The two password fields did not match."))

class _AccountForm(forms.ModelForm):
    facebook = forms.CharField(label='Facebook Username', max_length=64, validators=[models.UserLink.alphanumeric], required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(_AccountForm, self).__init__(*args, **kwargs)
        self.fields['accept_friend_requests'].widget = forms.CheckboxInput()
        self.fields['accept_friend_requests'].initial = True
        if self.request is not None:
            self.facebook_accounts_count = self.request.user.links.filter(type='facebook').count()
        if self.request is None or self.facebook_accounts_count > 0:
            del(self.fields['facebook'])

    def save(self, commit=True):
        instance = super(_AccountForm, self).save(commit=False)
        if self.request is not None:
            if 'facebook' in self.cleaned_data and self.cleaned_data['facebook']:
                models.UserLink.objects.create(owner=self.request.user, type='facebook', value=self.cleaned_data['facebook'])
            elif self.facebook_accounts_count <= 0:
                instance.accept_friend_requests = None
        if commit:
            instance.save()
        return instance

class SimpleAccountForm(_AccountForm):
    class Meta:
        model = models.Account
        fields = ('nickname', 'facebook', 'accept_friend_requests')

class AccountForm(_AccountForm):
    class Meta:
        model = models.Account
        fields = ('nickname', 'rank', 'os', 'device', 'play_with', 'account_id', 'facebook', 'accept_friend_requests')

class ConfirmDelete(forms.Form):
    confirm = forms.BooleanField(required=True, initial=False)
    thing_to_delete = forms.IntegerField(widget=forms.HiddenInput, required=True)

class FilterCardForm(forms.ModelForm):
    attributes = forms.MultipleChoiceField(choices=list(models.ATTRIBUTES), required=False)
    search = forms.CharField(required=False)
    ordering = forms.ChoiceField(choices=[
        ('creation', _('Creation')),
        ('performer__name', _('Performer')),
        ('type', _('Type of card')),
        ('rarity', _('Rarity')),
    ], initial='creation', required=False)
    reverse_order = forms.BooleanField(initial=True, required=False)

    def __init__(self, *args, **kwargs):
        super(FilterCardForm, self).__init__(*args, **kwargs)
        self.fields['type'].required = False
        self.fields['performer'].required = False

    class Meta:
        model = models.Card
        fields = ('type', 'performer', 'rarity', 'skill')

class FilterUserForm(forms.ModelForm):
    search = forms.CharField(required=False)
    favorite_performer = forms.ModelChoiceField(queryset=models.Performer.objects.all(), required=False)
    accept_friend_requests = forms.ChoiceField(choices=(BLANK_CHOICE_DASH + list(((2, _('Yes')), (3, _('No'))))), required=False)
    ordering = forms.ChoiceField(choices=[
        ('rank', _('Rank')),
        ('owner__date_joined', _('Creation')),
        ('owner__username', _('Username')),
        ('nickname', _('Nickname')),
    ], initial='rank', required=False)
    reverse_order = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = models.Account
        fields = ('favorite_performer', 'os', 'accept_friend_requests')

class CardForm(forms.ModelForm):
    type = 'reward'
    def save(self, commit=True):
        instance = super(CardForm, self).save(commit=False)
        instance.type = self.type
        if commit:
            instance.save()
        return instance

class RewardCardForm(CardForm):
    type = 'reward'
    class Meta:
        model = models.Card
        fields = ('image', 'rarity', 'sentence', 'reward_type', 'add_value')

class BoostCardForm(CardForm):
    type = 'boost'

    def __init__(self, *args, **kwargs):
        super(BoostCardForm, self).__init__(*args, **kwargs)
        self.fields['performer'].required = False

    class Meta:
        model = models.Card
        fields = ('image', 'rarity', 'sentence', 'add_value', 'performer')

class UnlockCardForm(CardForm):
    attributes = forms.MultipleChoiceField(choices=list(models.ATTRIBUTES), required=False)
    type = 'unlock'

    def save(self, commit=True):
        instance = super(UnlockCardForm, self).save(commit=False)
        instance.attributes = ','.join(self.cleaned_data['attributes'])
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.Card
        fields = ('image', 'rarity', 'performer', 'attributes', 'name', 'sentence', 'max_level', 'minimum_performance', 'maximum_performance', 'max_level_reward', 'skill', 'skill_value', 'trigger_value', 'trigger_chance')

class StageUpCardForm(CardForm):
    type = 'stageup'

    def __init__(self, *args, **kwargs):
        super(StageUpCardForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = self.fields['parent'].queryset.filter(type='unlock')

    class Meta:
        model = models.Card
        fields = ('parent', 'image', 'stage_number', 'sentence', 'maximum_performance', 'max_level')

cardTypeForms = {
    'reward': RewardCardForm,
    'boost': BoostCardForm,
    'unlock': UnlockCardForm,
    'stageup': StageUpCardForm,
}
