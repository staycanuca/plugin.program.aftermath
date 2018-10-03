MODULEID = {
	'yoda': {
		'name'     : 'Yoda',
		'plugin'   : 'plugin.video.yoda',
		'saved'    : 'yoda',
		'path'     : os.path.join(ADDONS, 'plugin.video.yoda'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.yoda', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.yoda', 'fanart.jpg'),
		'file'     : os.path.join(DATAFOLD, 'yoda_data'),
		'settings' : os.path.join(ADDOND, 'plugin.video.yoda', 'settings.xml'),
		'default'  : '',
		'data'     : [''],
		'activate' : 'RunPlugin(plugin://plugin.video.yoda/?action=authTrakt)'}
}
