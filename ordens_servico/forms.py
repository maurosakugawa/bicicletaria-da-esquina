from django import forms
from django.forms import inlineformset_factory
from .models import OrdemServico, ProdutoOrdemServico

class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = ['cliente', 'descricao_servico', 'status']
        widgets = {
            'cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do cliente'}),
            'descricao_servico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva o serviço realizado',
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class ProdutoOrdemServicoForm(forms.ModelForm):
    class Meta:
        model = ProdutoOrdemServico
        fields = ['produto', 'quantidade']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control produto-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control quantidade-input'}),
        }



# Inline Formset para associar vários produtos a uma Ordem de Serviço
ProdutoOrdemServicoFormSet = inlineformset_factory(
    OrdemServico,
    ProdutoOrdemServico,
    form=ProdutoOrdemServicoForm,
   # extra=1,
    extra=4,
    can_delete=True 
)
