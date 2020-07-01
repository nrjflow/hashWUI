from django.urls import path
import hashcat.views.api as api
import hashcat.views.gui as gui

urlpatterns = [
	path('api/crack/<int:hashType>/<int:attackMode>', api.crack, name='crack'),
	path('api/crack_status/<int:crackTaskId>', api.crackTaskStatus, name='crackStatus'),
	
    path('status/<int:crackTaskId>', gui.status, name='status'),
    path('new', gui.new, name='new'),
    path('home', gui.home, name='home'),
	path('', gui.home, name='home')
]
