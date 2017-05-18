	(function () {
		var ChatWindow = __class__ ('ChatWindow', [object], {
			get timenow () {return __get__ (this, function () {
				return ('[' + datetime.now ().strftime ('%H:%M:%S')) + ']';
			});},
			get toMD5 () {return __get__ (this, function (strtohash) {
				var MD5Hash = hashlib.md5 (strtohash).hexdigest ();
				return MD5Hash;
			});},
			get longcallback () {return __get__ (this, function () {
				print ('CB');
				var msg = document.getElementById ('text_1').innerHTML;
				var c = msg.__getslice__ (0, 150, 1);
				var outtext = '';
				var __iterable0__ = c;
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var letter = __iterable0__ [__index0__];
					if (letter != '\\') {
						var outtext = outtext + letter;
					}
				}
				document.getElementById ('text_1').innerHTML = outtext;
			});},
			get smallcallback () {return __get__ (this, function (msg) {
				var c = msg.py_get ().__getslice__ (0, 30, 1);
				var outtext = '';
				var __iterable0__ = c;
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var letter = __iterable0__ [__index0__];
					if (letter != '\\') {
						var outtext = outtext + letter;
					}
				}
				msg.set (outtext);
			});},
			get messagein () {return __get__ (this, function (mgdt) {
				Log (mgdt.decode ());
			});},
			get Log () {return __get__ (this, function (msg) {
				var msg = msg.py_replace ('\n', '<br>');
				document.getElementById ('frag_1').innerHTML = document.getElementById ('frag_1').innerHTML + msg;
			});},
			get sendmsg () {return __get__ (this, function (dts) {
				print ('sending ' + str (dts));
				var dtp = dts;
			});},
			get sendnewmessage () {return __get__ (this, function () {
				__globals__ (__all__) ['msgdata'] = document.getElementById ('text_1').innerHTML;
				if (msgdata.__getslice__ (0, 6, 1) == '~admin') {
					try {
						var msgdatatmp = msgdata.py_split (' -', 2);
						__globals__ (__all__) ['msgdata'] = (('~admin -' + msgdatatmp [1]) + ' -') + toMD5 (msgdatatmp [2].encode ());
					}
					catch (__except0__) {
						__globals__ (__all__) ['msgdata'] = '~admin';
					}
				}
				else if (msgdata.__getslice__ (0, 9, 1) == '~shutdown' || msgdata.__getslice__ (0, 8, 1) == '~restart') {
					try {
						var msgdatatmp = msgdata.py_split (' -', 1);
						__globals__ (__all__) ['msgdata'] = (msgdatatmp [0] + ' -') + toMD5 (msgdatatmp [1].encode ());
					}
					catch (__except0__) {
						__globals__ (__all__) ['msgdata'] = msgdatatmp [0];
					}
				}
				sendmsg (msgdata.encode ());
				document.getElementById ('text_1').innerHTML = '';
			});},
			get __init__ () {return __get__ (this, function (self) {
				try {
					var open = false;
					var firsttime = true;
					var connected = false;
					__globals__ (__all__) ['disconnected'] = false;
					while (!(__globals__ (__all__) ['disconnected'])) {
						if (!(connected)) {
							var hostserv = 'ws://PCOWNER:9009/';
							try {
								print ('connect with ' + str (hostserv));
								sendmsg ('cf7bcef89b9cf428535a77d5bdc972c8'.encode ());
								time.sleep (0.5);
								sendmsg ('test1'.encode ());
								time.sleep (0.5);
								sendmsg (os.getlogin ().encode ());
								time.sleep (0.5);
								sendmsg (platform.node ().encode ());
								var message = 'Connected to remote host. You can start sending messages.';
								var message = message + '\n';
								Log (message);
								var message = 'Type ~help to view commands.';
								var message = message + '\n';
								Log (message);
								var connected = true;
							}
							catch (__except0__) {
								if (isinstance (__except0__, Exception)) {
									var ex = __except0__;
									Log ('Unable to connect.\n');
									print ('A Connection Error Occured: ' + str (ex));
								}
								else {
									throw __except0__;
								}
							}
						}
					}
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
		__pragma__ ('<all>')
			__all__.ChatWindow = ChatWindow;
		__pragma__ ('</all>')
	}) ();
