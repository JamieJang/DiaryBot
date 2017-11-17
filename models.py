from django.db import models

class Writer(models.Model):
	name = models.CharField(max_length=1024)

	def __str__(self):
		return self.name

class Diary(models.Model):
	owner = models.ForeignKey(Writer,on_delete=models.CASCADE)
	date = models.DateField(auto_now_add=True)
	daily = models.TextField()

	def __str__(self):
		return '{} {}'.format(self.date,self.daily)

	class Meta:
		ordering = ['date']
