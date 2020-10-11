from django.db import models

# Create your models here.
class URL(models.Model):
    redirect = models.CharField(max_length=150)
    expired = models.DateField()
    view_count = models.IntegerField()

    def get_absolute_url(self):
        """Method called automatically when we return a redirect for this model"""
        return self.redirect

    def get_id_as_base(self, base=35):
        """This function exists so urls can have an integer primary key
        in the database (required by django's ORM) but still be identified
        by a short number in the actual url.
        """
        num = self.id
        output = ""
        while num > 0:
            next_digit = num % base
            if next_digit < 10:
                output += str(next_digit)
            else:
                output += chr(ord('A') + next_digit - 10)
            num //= base

        # We build the number backward so we reverse it before returning
        return output[::-1]
        
