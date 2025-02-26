# blog/forms.py
from django import forms
from . import models

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            img = Image.open(image)

            # Définition des dimensions maximales (ex: 800x800)
            max_size = (800, 800)
            img.thumbnail(max_size, Image.LANCZOS)

            # Sauvegarde de l’image compressée dans un buffer mémoire
            output = BytesIO()
            img.save(output, format='JPEG', quality=80)  # Qualité réduite à 80%
            output.seek(0)

            # Remplacement de l’image originale par l’image compressée
            image = InMemoryUploadedFile(
                output, 'ImageField', image.name, 'image/jpeg', sys.getsizeof(output), None
            )

        return image


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']