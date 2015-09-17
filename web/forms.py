from django import forms
from web import models
from django.utils.translation import ugettext_lazy as _, string_concat

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

class CardForm(forms.ModelForm):
    type = 'reward'
    def save(self, commit=True):
        instance = super(CardForm, self).save(commit=False)
        instance.type = self.type
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.Card

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
