# deck/forms.py
from django import forms
from .models import Deck, Card

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name']

class CardForm(forms.ModelForm):
    key_card_count = forms.IntegerField(min_value=1, initial=1, label="重要カード枚数", required=False)
    class Meta:
        model = Card
        fields = ['name', 'category', 'count','is_key_card','key_card_count']
        labels = {
            'name': 'カード名',
            'count': 'デッキ登録枚数',
            'is_key_card': '重要カードとして登録',
            'key_card_count': '重要カード枚数'
        }
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'is_key_card': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'key_card_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_key_card'].label = "重要カードとして登録"  # チェックボックスラベルの変更

    category = forms.ChoiceField(choices=Card.CATEGORY_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    count = forms.IntegerField(min_value=1, max_value=4, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))

def clean(self):
        cleaned_data = super().clean()
        is_key_card = cleaned_data.get('is_key_card')
        key_card_count = cleaned_data.get('key_card_count')
        count = cleaned_data.get('count')

        if is_key_card and key_card_count > count:
            raise forms.ValidationError("重要カード枚数はデッキ登録枚数以下にしてください。")

        return cleaned_data



class CardEditForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['name', 'category', 'count']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 60}),
        }


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name']  # デッキ名のみ編集可能        

class CardKeyForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['is_key_card', 'key_card_count']        


class AddCardForm(forms.Form):
    card = forms.ModelChoiceField(queryset=Card.objects.all(), label="カードを選択")
        