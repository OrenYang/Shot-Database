from django.db import models
from django.urls import reverse


def image_upload_dir(instance, filename):
    return 'images/{}/{}'.format(instance.name, filename)

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

    gasConfig = models.ForeignKey(GasConfig, on_delete=models.PROTECT, null=True, related_name='shot')
    outer_press = models.FloatField(null=True, blank=True)
    inner_press = models.FloatField(null=True, blank=True)
    target_press = models.FloatField(null=True, blank=True)
    outer_timing = models.IntegerField(null=True, blank=True)
    inner_timing = models.IntegerField(null=True, blank=True)
    target_timing = models.IntegerField(null=True, blank=True)

    current = models.FloatField(null=True, blank=True)
    current_time = models.FloatField(null=True, blank=True)
    dip_time = models.FloatField(null=True, blank=True)

    cavity_v = models.FloatField(null=True, blank=True, default=60)
    cavity_p = models.FloatField(null=True, blank=True, default=77)
    trigger_v = models.FloatField(null=True, blank=True, default=60)
    trigger_p = models.FloatField(null=True, blank=True, default=35)
    maxwell_p = models.FloatField(null=True, blank=True, default=60)
    premag_v = models.FloatField(null=True, blank=True)
    premag_t = models.FloatField(null=True, blank=True)
    pressure = models.FloatField(null=True, blank=True)

    def __str__(self):
        con = str(self.gasConfig)
        return 'Shot {}: {}'.format(self.num, con.split(':')[1])

    def get_absolute_url(self):
        return reverse('shot-detail', args=[str(self.num)])


class Filter(models.Model):

    mat = models.CharField(max_length=50)
    thickness = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.mat

class XrayDetector(models.Model):

    shot = models.ForeignKey(Shot, on_delete=models.CASCADE, related_name='xrayDetector', null=True)
    num = models.IntegerField(null=True, blank=True)
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE, related_name='xrayDetector', null=True)

    start = models.FloatField(null=True, blank=True)
    peak_time = models.FloatField(null=True, blank=True)
    peak_volt = models.FloatField(null=True, blank=True)

    def __str__(self):
        return 'XD{} from shot {}'.format(self.num, self.shot.num)


class XuvImage(models.Model):

    name = 'xuv'
    shot = models.ForeignKey(Shot, on_delete=models.CASCADE, related_name='xuvImage', null=True)
    num = models.IntegerField(null=True, blank=True)
    charge = models.FloatField(null=True, blank=True)

    frame1 = models.FloatField(null=True, blank=True)
    frame2 = models.FloatField(null=True, blank=True)
    frame3 = models.FloatField(null=True, blank=True)
    frame4 = models.FloatField(null=True, blank=True)

    image = models.ImageField(upload_to=image_upload_dir, null=True, blank=True)

    def __str__(self):
        return 'XUV Camera {} from shot {}'.format(self.num, self.shot.num)
