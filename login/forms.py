from django import forms
from django.contrib.auth.models import User
from .models import Proyecto, Usuario

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ('nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'product_owner', 'scrum_master', 'team_members')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_owner'].queryset = Usuario.objects.all()
        self.fields['scrum_master'].queryset = Usuario.objects.all()
        self.fields['team_members'].queryset = Usuario.objects.all()
class AgregarUsuariosForm(forms.Form):
    product_owner = forms.ModelChoiceField(queryset=User.objects.all(), label='Product Owner')
    scrum_master = forms.ModelChoiceField(queryset=User.objects.all(), label='Scrum Master')
    team_members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label='Team Members')

    def __init__(self, *args, **kwargs):
        self.proyecto = kwargs.pop('proyecto')
        super(AgregarUsuariosForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(AgregarUsuariosForm, self).clean()

        product_owner = cleaned_data.get('product_owner')
        scrum_master = cleaned_data.get('scrum_master')
        team_members = cleaned_data.get('team_members')

        if product_owner == scrum_master or product_owner in team_members or scrum_master in team_members:
            raise forms.ValidationError('Un usuario no puede ser Product Owner y Scrum Master al mismo tiempo ni estar en ambos roles.')

        return cleaned_data
