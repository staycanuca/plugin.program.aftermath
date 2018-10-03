################################################################################
#      Copyright (C) 2015 Surfacingx                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import uservar
import time
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from datetime import date, datetime, timedelta
from resources.libs import wizard as wiz
from resources.libs.modules import * as modules

ADDON_ID       = uservar.ADDON_ID
ADDONTITLE     = uservar.ADDONTITLE
ADDON          = wiz.addonId(ADDON_ID)
DIALOG         = xbmcgui.Dialog()
HOME           = xbmc.translatePath('special://home/')
ADDONS         = os.path.join(HOME,      'addons')
USERDATA       = os.path.join(HOME,      'userdata')
PLUGIN         = os.path.join(ADDONS,    ADDON_ID)
PACKAGES       = os.path.join(ADDONS,    'packages')
ADDONDATA      = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADDOND         = os.path.join(USERDATA,  'addon_data')
DATAFOLD      = os.path.join(ADDONDATA, 'data')
ICON           = os.path.join(PLUGIN,    'icon.png')
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
THREEDAYS      = TODAY + timedelta(days=3)
KEEPMODULE      = wiz.getS('keepmodule')
MODULESAVE      = wiz.getS('modulelastsave')
COLOR1         = uservar.COLOR1
COLOR2         = uservar.COLOR2
ORDER          = moduleOrder()

def moduleOrder():
	array = []
	for module in modules:
		array.append(module.MODULEID)
	return array

def moduleUser(who):
    user=None
	if moduleId(who):
		if os.path.exists(moduleId(who))['path']):
			try:
				add = wiz.addonId(moduleId(who))['plugin'])
				user = add.getSetting(moduleId(who)['default'])
			except:
				return None
	return user

def moduleId(module):
	MODULEID = modules[ORDER.index(module)]]
	return MODULEID

def moduleIt(do, who):
	if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
	if not os.path.exists(DATAFOLD): os.makedirs(DATAFOLD)
	if who == 'all':
		for log in ORDER:
			if os.path.exists(moduleID(log)['path']):
				try:
					addonid   = wiz.addonId(moduleID(log)['plugin'])
					default   = moduleId(log)['default']
					user      = addonid.getSetting(default)
					if user == '' and do == 'update': continue
					updateModule(do, log)
				except: pass
			else: wiz.log('[Module Data] %s(%s) is not installed' % moduleId(log)['name'], moduleId(log)['plugin']), xbmc.LOGERROR)
		wiz.setS('modulelastsave', str(THREEDAYS))
	else:
		if moduleId(who):
			if os.path.exists(moduleId(who)['path']):
				updateModule(do, who)
		else: wiz.log('[Module Data] Invalid Entry: %s' % who, xbmc.LOGERROR)

def clearSaved(who, over=False):
	if who == 'all':
		for module in MODULEID:
			clearSaved(module,  True)
	elif MODULEID[who]:
		file = MODULEID[who]['file']
		if os.path.exists(file):
			os.remove(file)
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, MODULEID[who]['name']),'[COLOR %s]Module Data: Removed![/COLOR]' % COLOR2, 2000, MODULEID[who]['icon'])
		wiz.setS(MODULEID[who]['saved'], '')
	if over == False: wiz.refresh()

def updateModule(do, who):
	file      = MODULEID[who]['file']
	settings  = MODULEID[who]['settings']
	data      = MODULEID[who]['data']
	addonid   = wiz.addonId(MODULEID[who]['plugin'])
	saved     = MODULEID[who]['saved']
	default   = MODULEID[who]['default']
	user      = addonid.getSetting(default)
	suser     = wiz.getS(saved)
	name      = MODULEID[who]['name']
	icon      = MODULEID[who]['icon']

	if do == 'update':
		if not user == '':
			try:
				with open(file, 'w') as f:
					for module in data:
						f.write('<data>\n\t<id>%s</id>\n\t<value>%s</value>\n</data>\n' % (module, addonid.getSetting(module)))
					f.close()
				user = addonid.getSetting(default)
				wiz.setS(saved, user)
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name), '[COLOR %s]Module Data: Saved![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Module Data] Unable to Update %s (%s)" % (who, str(e)), xbmc.LOGERROR)
		else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name), '[COLOR %s]Module Data: Not Registered![/COLOR]' % COLOR2, 2000, icon)
	elif do == 'restore':
		if os.path.exists(file):
			f = open(file,mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			match = re.compile('<data><id>(.+?)</id><value>(.+?)</value></data>').findall(g)
			try:
				if len(match) > 0:
					for module, value in match:
						addonid.setSetting(module, value)
				user = addonid.getSetting(default)
				wiz.setS(saved, user)
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name), '[COLOR %s]Module: Restored![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Module Data] Unable to Restore %s (%s)" % (who, str(e)), xbmc.LOGERROR)
		#else: wiz.LogNotify(name,'Trakt Data: [COLOR red]Not Found![/COLOR]', 2000, icon)
	elif do == 'clearaddon':
		wiz.log('%s SETTINGS: %s' % (name, settings), xbmc.LOGDEBUG)
		if os.path.exists(settings):
			try:
				f = open(settings, "r"); lines = f.readlines(); f.close()
				f = open(settings, "w")
				for line in lines:
					match = wiz.parseDOM(line, 'setting', ret='id')
					if len(match) == 0: f.write(line)
					else:
						if match[0] not in data: f.write(line)
						else: wiz.log('Removing Line: %s' % line, xbmc.LOGNOTICE)
				f.close()
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name),'[COLOR %s]Addon Data: Cleared![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Module Data] Unable to Clear Addon %s (%s)" % (who, str(e)), xbmc.LOGERROR)
	wiz.refresh()

def autoUpdate(who):
	if who == 'all':
		for log in MODULEID:
			if os.path.exists(MODULEID[log]['path']):
				autoUpdate(log)
	elif MODULEID[who]:
		if os.path.exists(MODULEID[who]['path']):
			u  = moduleUser(who)
			su = wiz.getS(MODULEID[who]['saved'])
			n = MODULEID[who]['name']
			if u == None or u == '': return
			elif su == '': moduleIt('update', who)
			elif not u == su:
				if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to save the [COLOR %s]Module[/COLOR] data for [COLOR %s]%s[/COLOR]?" % (COLOR2, COLOR1, COLOR1, n), "Addon: [COLOR springgreen][B]%s[/B][/COLOR]" % u, "Saved:[/COLOR] [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]', yeslabel="[B][COLOR springgreen]Save Data[/COLOR][/B]", nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
					moduleIt('update', who)
			else: moduleIt('update', who)

def importlist(who):
	if who == 'all':
		for log in MODULEID:
			if os.path.exists(MODULEID[log]['file']):
				importlist(log)
	elif MODULEID[who]:
		if os.path.exists(MODULEID[who]['file']):
			d  = MODULEID[who]['default']
			sa = MODULEID[who]['saved']
			su = wiz.getS(sa)
			n  = MODULEID[who]['name']
			f  = open(MODULEID[who]['file'],mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			m  = re.compile('<data><id>%s</id><value>(.+?)</value></data>' % d).findall(g)
			if len(m) > 0:
				if not m[0] == su:
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to import the [COLOR %s]Module[/COLOR] data for [COLOR %s]%s[/COLOR]?" % (COLOR2, COLOR1, COLOR1, n), "File: [COLOR springgreen][B]%s[/B][/COLOR]" % m[0], "Saved:[/COLOR] [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]', yeslabel="[B]Save Data[/B]", nolabel="[B]No Cancel[/B]"):
						wiz.setS(sa, m[0])
						wiz.log('[Import Data] %s: %s' % (who, str(m)), xbmc.LOGNOTICE)
					else: wiz.log('[Import Data] Declined Import(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)
				else: wiz.log('[Import Data] Duplicate Entry(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)
			else: wiz.log('[Import Data] No Match(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)

def activateModule(who):
	if MODULEID[who]:
		if os.path.exists(MODULEID[who]['path']):
			act     = MODULEID[who]['activate']
			addonid = wiz.addonId(MODULEID[who]['plugin'])
			if act == '': addonid.openSettings()
			else: url = xbmc.executebuiltin(MODULEID[who]['activate'])
		else: DIALOG.ok(ADDONTITLE, '%s is not currently installed.' % MODULEID[who]['name'])
	else:
		wiz.refresh()
		return
	check = 0
	while moduleUser(who) == None:
		if check == 30: break
		check += 1
		time.sleep(10)
	wiz.refresh()
