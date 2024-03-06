from django.db import models
from django.urls import reverse


def image_upload_dir(instance, filename):
    return 'images/{}/{}'.format(instance.diagnostic, filename)

def config(self):
    config=''
    if self.outer is not None and self.inner is not None:
        config += 'Double liner'
    elif (self.outer is not None and self.inner is None) or (self.inner is not None and self.outer is None):
        config += 'Single liner'
    if config != '':
        if self.target is None:
            config += ' only'
        else:
            config += ' on target'
    if config == '' and self.target is not None:
        config += 'Target only'
    return config



class Gas(models.Model):

    gas = models.CharField(max_length=20)
    chemical_symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.gas


class GasConfig(models.Model):

            outer = models.ForeignKey(Gas, on_delete=models.CASCADE, null=True, blank=True, related_name='outer')
            inner = models.ForeignKey(Gas, on_delete=models.CASCADE, null=True, blank=True, related_name='inner')
            target = models.ForeignKey(Gas, on_delete=models.CASCADE, null=True, blank=True, related_name='target')

            def __str__(self):
                con = config(self)+': '
                nozzles = [self.outer, self.inner, self.target]
                for i in range(len(nozzles)):
                    if nozzles[i] is not None:
                        con += '{}/'.format(nozzles[i].chemical_symbol)
                return con[:-1]


class Shot(models.Model):

    time = models.DateTimeField()
    num = models.IntegerField(null=True, blank=True)
    gasConfig = models.ForeignKey(GasConfig, on_delete=models.PROTECT, null=True, related_name='gasConfig')
    current = models.FloatField(null=True, blank=True)

    outer_press = models.FloatField(null=True, blank=True)
    inner_press = models.FloatField(null=True, blank=True)
    target_press = models.FloatField(null=True, blank=True)
    outer_timing = models.IntegerField(null=True, blank=True)
    inner_timing = models.IntegerField(null=True, blank=True)
    target_timing = models.IntegerField(null=True, blank=True)


    def __str__(self):
        con = str(self.gasConfig)
        return 'Shot {}: {}'.format(self.num, con.split(':')[1])

    def get_absolute_url(self):
        return reverse('shot-detail', args=[str(self.num)])


class DiagnosticImage(models.Model):

    choices = [
        ('xuv','xuv'),
        ('schlieren','schlieren'),
        ('other','other'),
    ]

    diagnostic = models.CharField(max_length=20,
                                  choices=choices,
                                  default='other',)
    shot = models.ForeignKey(Shot, on_delete=models.CASCADE, related_name='shot', null=True)
    comments = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=image_upload_dir)

    def __str__(self):
        return '{} image from shot {}'.format(self.diagnostic, self.shot.num)

    def get_absolute_url(self):
        return reverse('shot-detail', kwargs={'pk': self.shot.pk})
