	(function () {
		var nodejs = {};
		var Test = __class__ ('Test', [object], {
			get __init__ () {return __get__ (this, function (self) {
				__nest__ (nodejs, '', __init__ (__world__.nodejs));
				print ('HI');
				try {
					// pass;
				}
				catch (__except0__) {
					if (isinstance (__except0__, Exception)) {
						var ex = __except0__;
						print ('Error: ' + str (ex));
					}
					else {
						throw __except0__;
					}
				}
			});}
		});
		__pragma__ ('<use>' +
			'nodejs' +
		'</use>')
		__pragma__ ('<all>')
			__all__.Test = Test;
		__pragma__ ('</all>')
	}) ();
