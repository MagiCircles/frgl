from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import BLANK_CHOICE_DASH
from web import models, raw
from django.utils.translation import ugettext_lazy as _, string_concat

class _UserCheckEmailForm(forms.ModelForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def __init__(self, *args, **kwargs):
        super(_UserCheckEmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

class CreateUserForm(_UserCheckEmailForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

class UserForm(_UserCheckEmailForm):
    class Meta:
        model = User
        fields = ('email',)

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
    facebook = forms.CharField(label='Facebook Username', max_length=64, validators=[models.UserLink.alphanumeric], required=False, help_text=_('Make sure you write your username and not your full name. Your username appears in the URL of your Facebook profile.'))

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
        fields = ('nickname', 'rank', 'stars', 'os', 'device', 'play_with', 'account_id', 'facebook', 'accept_friend_requests')

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
        self.fields['rarity'].choices = BLANK_CHOICE_DASH + list(models.RARITY)
        self.fields['rarity'].initial = False
        self.fields['rarity'].required = False
        self.fields['type'].required = False
        self.fields['performer'].required = False
        self.fields['skill'].help_text = None

    class Meta:
        model = models.Card
        fields = ('search', 'type', 'performer', 'rarity', 'skill', 'attributes', 'ordering', 'reverse_order')

class FilterUserForm(forms.ModelForm):
    search = forms.CharField(required=False)
    favorite_performer = forms.ModelChoiceField(queryset=models.Performer.objects.all(), required=False)
    ordering = forms.ChoiceField(choices=[
        ('stars', _('Stars')),
        ('rank', _('Rank')),
        ('owner__date_joined', _('Creation')),
        ('owner__username', _('Username')),
        ('nickname', _('Nickname')),
    ], initial='stars', required=False)
    reverse_order = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = models.Account
        fields = ('search', 'favorite_performer', 'os', 'accept_friend_requests')

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
    song_types = forms.MultipleChoiceField(choices=list(models.ATTRIBUTES), required=False, label=_('Song types'))
    type = 'unlock'

    def __init__(self, *args, **kwargs):
        super(UnlockCardForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['song_types'].initial = kwargs['instance'].attributes.split(',')

    def save(self, commit=True):
        instance = super(UnlockCardForm, self).save(commit=False)
        instance.attributes = ','.join(self.cleaned_data['song_types'])
        instance.children.all().update(rarity=instance.rarity, performer=instance.performer, attributes=instance.attributes)
        if instance.rarity == 'C':
            instance.skill = None
            instance.skill_value = None
            instance.trigger_value = None
            instance.trigger_chance = None
        if instance.rarity == 'C' or instance.rarity == 'R':
            instance.maximum_performance_ability = None
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.Card
        fields = ('image', 'rarity', 'performer', 'song_types', 'name', 'sentence', 'maximum_performance_ability', 'skill', 'skill_value', 'trigger_value', 'trigger_chance', 'how_to_obtain')

class StageUpCardForm(CardForm):
    type = 'stageup'

    def __init__(self, *args, **kwargs):
        super(StageUpCardForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = self.fields['parent'].queryset.filter(type='unlock').order_by('rarity', 'name', 'performer__name')

    def clean(self):
        if 'stage_number' in self.cleaned_data:
            parent = self.cleaned_data['parent']
            max_stage_number_for_rarity = raw.cards_data[parent.rarity]['stages']
            if self.cleaned_data['stage_number'] > max_stage_number_for_rarity:
                raise forms.ValidationError(_('The maximum stage number for {} card is {}.').format(parent.rarity, max_stage_number_for_rarity))
        return self.cleaned_data

    def save(self, commit=True):
        instance = super(StageUpCardForm, self).save(commit=False)
        instance.rarity = instance.parent.rarity
        instance.performer = instance.parent.performer
        instance.attributes = instance.parent.attributes
        if instance.rarity == 'C' or instance.rarity == 'R':
            instance.maximum_performance_ability = None
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.Card
        fields = ('parent', 'image', 'stage_number', 'sentence', 'maximum_performance_ability', 'skill_value')

cardTypeForms = {
    'reward': RewardCardForm,
    'boost': BoostCardForm,
    'unlock': UnlockCardForm,
    'stageup': StageUpCardForm,
}
