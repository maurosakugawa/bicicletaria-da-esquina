from django import forms
from django.forms import inlineformset_factory
from .models import OrdemServico, ProdutoOrdemServico

class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = ['cliente', 'descricao_servico', 'valor_total', 'status']
        exclude = ['funcionario']  # Exclui o campo funcionário

        widgets = {
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao_servico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        
class ProdutoOrdemServicoForm(forms.ModelForm):
    class Meta:
        model = ProdutoOrdemServico
        fields = ['produto', 'quantidade']

ProdutoOrdemServicoFormSet = inlineformset_factory(OrdemServico, ProdutoOrdemServico, form=ProdutoOrdemServicoForm, extra=1)        
