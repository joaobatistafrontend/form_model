from django import forms
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

class ContatoForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    opcoes = forms.ChoiceField(
        choices=[
            ('Unidade de Placa de Carro', 'Unidade de Placa de Carro'),
            ('Par de Placa de Carro', 'Par de Placa de Carro'),
            ('Placa de Moto', 'Placa de Moto'),
        ],
        label="Opções de Agendamento"
    )
    horario = forms.ChoiceField(
        choices=[
            (f"{hour:02d}:{minute:02d}", f"{hour:02d}:{minute:02d}")
            for hour in range(8, 16) for minute in (0, 30)
        ],
        label="Selecione um horário"
    )
    local = forms.ChoiceField(
        choices = [
            ('Fortaleza - CE: Godofredo Maciel, 2743-A - Jardim Cearense','Fortaleza - CE: Godofredo Maciel, 2743-A - Jardim Cearense'),
            ('Fortaleza - CE: Gustavo Sampaio, 1293 - Parquelândia', 'Fortaleza - CE: Gustavo Sampaio, 1293 - Parquelândia'),
            ('Guaraciaba do Norte - CE: Av. 12 de Novembro, 50 - Centro','Guaraciaba do Norte - CE: Av. 12 de Novembro, 50 - Centro'),
            ('Quixeré - CE: R. Mte. Felipe, 917 - Centro', 'Quixeré - CE: R. Mte. Felipe, 917 - Centro'),
            ('Itapajé - CE : R. Jandira Bastos Magalhães, 689', 'Itapajé - CE : R. Jandira Bastos Magalhães, 689')
        ],
        label='Opções de locais'
    )
    data = forms.DateField(
        label='Data de Agendamento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
     
    def send_email(self):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        opcoes = self.cleaned_data['opcoes']
        horario = self.cleaned_data['horario']
        local = self.cleaned_data['local']
        data = self.cleaned_data['data']
        assunto = 'Marca visita'

        # Criação de um arquivo PDF com os dados do formulário
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph('Comprovante de Agendamento', styles['Title']))
        elements.append(Spacer(1, 12))

        data_table = [
            ['Nome:', nome],
            ['Email:', email],
            ['Opções de Agendamento:', opcoes],
            ['Horário:', horario],
            ['Local:', Paragraph(local, styles['Normal'])],  # Utilize o estilo 'Normal' para quebrar a linha
            ['Data de Agendamento:', data],
        ]

        table = Table(data_table, colWidths=300, rowHeights=30)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)

        # Anexa o PDF ao email
        buffer.seek(0)
        email = EmailMessage(
            subject=assunto,
            from_email='jbbuno007@gmail.com',
            to=[email],
        )
        email.attach('comprovante.pdf', buffer.read(), 'application/pdf')
        email.send()










'''from django import forms
from .models import DadosFormModels
from django.core.mail import EmailMessage

class ContatoForm(forms.Form):
     nome = forms.CharField(label='Nome', max_length=100)
     email = forms.EmailField(label='Email', max_length=100)
     #assunto = forms.ChoiceField(
          #choices=[
               #('marca', 'Marca Agendamento'),
          #],label='assunto'
     #)
     opcoes = forms.ChoiceField(
          choices=[
               ('Unidade de Placa de Carro', 'Unidade de Placa de Carro'),
               ('Par de Placa de Carro', 'Par de Placa de Carro'),
               ('Placa de Moto', 'Placa de Moto'),
          ],
          label="Opções de Agendamento"
     )
     horario = forms.ChoiceField(
          choices=[
               (f"{hour:02d}:{minute:02d}", f"{hour:02d}:{minute:02d}")
               for hour in range(8, 16) for minute in (0, 30)
          ],
          label="Selecione um horário"
          )
     local = forms.ChoiceField(
          choices = [
               ('Fortaleza - CE: Av. Godofredo Maciel, 2743-A - Jardim Cearense, Fortaleza - CE, 60710-001','Fortaleza - CE: Av. Godofredo Maciel, 2743-A - Jardim Cearense, Fortaleza - CE, 60710-001'),
               ('Fortaleza - CE: R. Gustavo Sampaio, 1293 - Parquelândia, Fortaleza - CE, 60455-001', 'Fortaleza - CE: R. Gustavo Sampaio, 1293 - Parquelândia, Fortaleza - CE, 60455-001'),
               ('Guaraciaba do Norte - CE: Av. 12 de Novembro, 50 - Centro, Guaraciaba do Norte - CE, 62380-000', 'Guaraciaba do Norte - CE: Av. 12 de Novembro, 50 - Centro, Guaraciaba do Norte - CE, 62380-000'),
               ('Quixeré - CE: R. Mte. Felipe, 917 - Centro, Quixeré - CE, 62920-000', 'Quixeré - CE: R. Mte. Felipe, 917 - Centro, Quixeré - CE, 62920-000'),
               ('Itapajé - CE : R. Jandira Bastos Magalhães, 689 - Itapajé, CE, 62600-000', 'Itapajé - CE : R. Jandira Bastos Magalhães, 689 - Itapajé, CE, 62600-000')
          ],
          label='Opções de locais'
     )
     data = forms.DateField(
          label='Data de Agendamento',
          widget=forms.DateInput(attrs={'type': 'date'})
     )
     
     def send_email(self):
          nome = self.cleaned_data['nome']
          email = self.cleaned_data['email']
          opcoes = self.cleaned_data['opcoes']
          horario = self.cleaned_data['horario']
          local = self.cleaned_data['local']
          data = self.cleaned_data['data']
          assunto = 'Marca visita'
          corpo = f'Nome: {nome}\n Mensagem:{opcoes}\n Horario:{horario}\n Local:{local}\n Data:{data}'
          mail = EmailMessage(
               subject = assunto,
               from_email = 'jbbuno007@gmail.com',
               to = [email],
               body = corpo,
               headers = {
                    'Replay-To' : 'jbbuno007@gmail.com'
               }
          )
          mail.send()


'''



'''
class DadosForm(forms.ModelForm):
     class meta:
          model = DadosFormModels
          fields = ['nome', 'email', 'subject', 'msg']

     def __init__(self, *args,kwargs):
          super().__init__(*args,kwargs)
          for fild_name, field in self.fields.items():
               field.widget.atts['class'] = 'form-control'''