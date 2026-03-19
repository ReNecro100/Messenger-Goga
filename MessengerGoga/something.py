# Проверьте в shell:
from .models import User
user = aser.objects.get(username='2')
print(user.is_active)  # Должно быть True