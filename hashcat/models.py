from django.db import models
import datetime, uuid
from django.utils import timezone
# Create your models here.
class CrackingTask(models.Model):
	name = models.CharField(max_length=200, default="DefaultModelValue")
	status = models.IntegerField()
	speed = models.IntegerField()
	recoveredHashes = models.IntegerField()
	totalLoadedHashes = models.IntegerField()
	triedPasswords = models.IntegerField()
	totalPasswords = models.IntegerField()
	startDate = models.DateTimeField('date created', default=timezone.now)
	hashType = models.IntegerField()
	attackMode = models.IntegerField()
	sessionID = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	def statusText(self):
		switcher = {
			0: "Starting",
			3: "Running",
			5: "Exhausted",
			6: "Cracked",
			7: "Aborted",
			8: "Quit"
		}
		return switcher.get(self.status,"Invalid_Status")
	def progressPercent(self):
		if(self.status==6):
				return round(100, 2)
		if self.triedPasswords and self.totalPasswords:
				return round(int(self.triedPasswords)/int(self.totalPasswords)*100,2)
		else:
			return 0

	def estimatedTime(self):
		if self.triedPasswords and self.totalPasswords and self.speed:
			if(self.status==6):
				return 0
			else:
				return round((int(self.totalPasswords)-int(self.triedPasswords))/int(self.speed))
		else:
			return 0
	def attackModeText(self):
		switcher ={
			0: "Straight",
			1: "Combination",
			3: "Brute-force",
			6: "Hybrid Wordlist + Mask",
			7: "Hybrid Mask + Wordlist"
		}
		return switcher.get(self.attackMode,"Invalid_Attack_Mode")

	def hashTypeText(self):
		switcher = {
			0: "MD5",
			900: "MD4",
			5100: "Half MD5",
			100: "SHA1",
			1300: "SHA2-224",
			1400: "SHA2-256",
			10800: "SHA2-384",
			1700: "SHA2-512",
			17300: "SHA3-224",
			17400: "SHA3-256",
			17500: "SHA3-384",
			17600: "SHA3-512",
			17700: "Keccak-224",
			17800: "Keccak-256",
			17900: "Keccak-384",
			18000: "Keccak-512",
			600: "BLAKE2b-512",
			10100: "SipHash",
			6000: "RIPEMD-160",
			6100: "Whirlpool",
			6900: "GOST R 34.11-94",
			11700: "GOST R 34.11-2012 (Streebog) 256-bit, big-endian",
			11800: "GOST R 34.11-2012 (Streebog) 512-bit, big-endian",
			10: "md5($pass.$salt",
			20: "md5($salt.$pass",
			30: "md5(utf16le($pass).$salt",
			40: "md5($salt.utf16le($pass",
			3800: "md5($salt.$pass.$salt",
			3710: "md5($salt.md5($pass",
			4010: "md5($salt.md5($salt.$pass",
			4110: "md5($salt.md5($pass.$salt",
			2600: "md5(md5($pass",
			3910: "md5(md5($pass).md5($salt",
			4300: "md5(strtoupper(md5($pass",
			4400: "md5(sha1($pass",
			110: "sha1($pass.$salt",
			120: "sha1($salt.$pass",
			130: "sha1(utf16le($pass).$salt",
			140: "sha1($salt.utf16le($pass",
			4500: "sha1(sha1($pass",
			4520: "sha1($salt.sha1($pass",
			4700: "sha1(md5($pass",
			4900: "sha1($salt.$pass.$salt",
			14400: "sha1(CX",
			1410: "sha256($pass.$salt",
			1420: "sha256($salt.$pass",
			1430: "sha256(utf16le($pass).$salt",
			1440: "sha256($salt.utf16le($pass",
			1710: "sha512($pass.$salt",
			1720: "sha512($salt.$pass",
			1730: "sha512(utf16le($pass).$salt",
			1740: "sha512($salt.utf16le($pass",
			50: "HMAC-MD5 (key = $pass",
			60: "HMAC-MD5 (key = $salt",
			150: "HMAC-SHA1 (key = $pass",
			160: "HMAC-SHA1 (key = $salt",
			1450: "HMAC-SHA256 (key = $pass",
			1460: "HMAC-SHA256 (key = $salt",
			1750: "HMAC-SHA512 (key = $pass",
			1760: "HMAC-SHA512 (key = $salt",
			11750: "HMAC-Streebog-256 (key = $pass), big-endian",
			11760: "HMAC-Streebog-256 (key = $salt), big-endian",
			11850: "HMAC-Streebog-512 (key = $pass), big-endian",
			11860: "HMAC-Streebog-512 (key = $salt), big-endian",
			14000: "DES (PT = $salt, key = $pass",
			14100: "3DES (PT = $salt, key = $pass",
			14900: "Skip32 (PT = $salt, key = $pass",
			15400: "ChaCha20",
			400: "phpass",
			8900: "scrypt",
			11900: "PBKDF2-HMAC-MD5",
			12000: "PBKDF2-HMAC-SHA1",
			10900: "PBKDF2-HMAC-SHA256",
			12100: "PBKDF2-HMAC-SHA512",
			23: "Skype",
			2500: "WPA-EAPOL-PBKDF2",
			2501: "WPA-EAPOL-PMK",
			16800: "WPA-PMKID-PBKDF2",
			16801: "WPA-PMKID-PMK",
			4800: "iSCSI CHAP authentication, MD5(CHAP",
			5300: "IKE-PSK MD5",
			5400: "IKE-PSK SHA1",
			5500: "NetNTLMv1",
			5500: "NetNTLMv1+ESS",
			5600: "NetNTLMv2",
			7300: "IPMI2 RAKP HMAC-SHA1",
			7500: "Kerberos 5 AS-REQ Pre-Auth etype 23",
			8300: "DNSSEC (NSEC3",
			10200: "CRAM-MD5",
			11100: "PostgreSQL CRAM (MD5",
			11200: "MySQL CRAM (SHA1",
			11400: "SIP digest authentication (MD5",
			13100: "Kerberos 5 TGS-REP etype 23",
			16100: "TACACS",
			16500: "JWT (JSON Web Token",
			18200: "Kerberos 5 AS-REP etype 23",
			121: "SMF (Simple Machines Forum) > v1.1",
			400: "phpBB3 (MD5",
			2611: "vBulletin &lt; v3.8.5",
			2711: "vBulletin >= v3.8.5",
			2811: "MyBB 1.2",
			2811: "IPB2+ (Invision Power Board",
			8400: "WBB3 (Woltlab Burning Board",
			11: "Joomla &lt; 2.5.18",
			400: "Joomla >= 2.5.18 (MD5",
			400: "WordPress (MD5",
			2612: "PHPS",
			7900: "Drupal7",
			21: "osCommerce",
			21: "xt:Commerce",
			11000: "PrestaShop",
			124: "Django (SHA-1",
			10000: "Django (PBKDF2-SHA256",
			16000: "Tripcode",
			3711: "MediaWiki B type",
			13900: "OpenCart",
			4521: "Redmine",
			4522: "PunBB",
			12001: "Atlassian (PBKDF2-HMAC-SHA1",
			12: "PostgreSQL",
			131: "MSSQL (2000",
			132: "MSSQL (2005",
			1731: "MSSQL (2012, 2014",
			200: "MySQL323",
			300: "MySQL4.1/MySQL5",
			3100: "Oracle H: Type (Oracle 7",
			112: "Oracle S: Type (Oracle 11",
			12300: "Oracle T: Type (Oracle 12",
			8000: "Sybase ASE",
			141: "Episerver 6.x &lt; .NET 4",
			1441: "Episerver 6.x >= .NET 4",
			1600: "Apache $apr1$ MD5, md5apr1, MD5 (APR",
			12600: "ColdFusion 10",
			1421: "hMailServer",
			101: "nsldap, SHA-1(Base64), Netscape LDAP SHA",
			111: "nsldaps, SSHA-1(Base64), Netscape LDAP SSHA",
			1411: "SSHA-256(Base64), LDAP {SSHA256",
			1711: "SSHA-512(Base64), LDAP {SSHA512",
			16400: "CRAM-MD5 Dovecot",
			15000: "FileZilla Server >= 0.9.55",
			11500: "CRC32",
			3000: "LM",
			1000: "NTLM",
			1100: "Domain Cached Credentials (DCC), MS Cache",
			2100: "Domain Cached Credentials 2 (DCC2), MS Cache 2",
			15300: "DPAPI masterkey file v1",
			15900: "DPAPI masterkey file v2",
			12800: "MS-AzureSync  PBKDF2-HMAC-SHA256",
			1500: "descrypt, DES (Unix), Traditional DES",
			12400: "BSDi Crypt, Extended DES",
			500: "md5crypt, MD5 (Unix), Cisco-IOS $1$ (MD5",
			3200: "bcrypt $2*$, Blowfish (Unix",
			7400: "sha256crypt $5$, SHA256 (Unix",
			1800: "sha512crypt $6$, SHA512 (Unix",
			122: "macOS v10.4, MacOS v10.5, MacOS v10.6",
			1722: "macOS v10.7",
			7100: "macOS v10.8+ (PBKDF2-SHA512",
			6300: "AIX {smd5",
			6700: "AIX {ssha1",
			6400: "AIX {ssha256",
			6500: "AIX {ssha512",
			2400: "Cisco-PIX MD5",
			2410: "Cisco-ASA MD5",
			500: "Cisco-IOS $1$ (MD5",
			5700: "Cisco-IOS type 4 (SHA256",
			9200: "Cisco-IOS $8$ (PBKDF2-SHA256",
			9300: "Cisco-IOS $9$ (scrypt",
			22: "Juniper NetScreen/SSG (ScreenOS",
			501: "Juniper IVE",
			15100: "Juniper/NetBSD sha1crypt",
			7000: "FortiGate (FortiOS",
			5800: "Samsung Android Password/PIN",
			13800: "Windows Phone 8+ PIN/password",
			8100: "Citrix NetScaler",
			8500: "RACF",
			7200: "GRUB 2",
			9900: "Radmin2",
			125: "ArubaOS",
			7700: "SAP CODVN B (BCODE",
			7701: "SAP CODVN B (BCODE) via RFC_READ_TABLE",
			7800: "SAP CODVN F/G (PASSCODE",
			7801: "SAP CODVN F/G (PASSCODE) via RFC_READ_TABLE",
			10300: "SAP CODVN H (PWDSALTEDHASH) iSSHA-1",
			8600: "Lotus Notes/Domino 5",
			8700: "Lotus Notes/Domino 6",
			9100: "Lotus Notes/Domino 8",
			133: "PeopleSoft",
			13500: "PeopleSoft PS_TOKEN",
			11600: "7-Zip",
			12500: "RAR3-hp",
			13000: "RAR5",
			13200: "AxCrypt",
			13300: "AxCrypt in-memory SHA1",
			13600: "WinZip",
			14700: "iTunes backup &lt; 10.0",
			14800: "iTunes backup >= 10.0",
			6211: "TrueCrypt PBKDF2-HMAC-RIPEMD160 XTS 512 bit",
			6212: "TrueCrypt PBKDF2-HMAC-RIPEMD160 XTS 1024 bit",
			6213: "TrueCrypt PBKDF2-HMAC-RIPEMD160 XTS 1536 bit",
			6221: "TrueCrypt PBKDF2-HMAC-SHA512 XTS 512 bit",
			6222: "TrueCrypt PBKDF2-HMAC-SHA512 XTS 1024 bit",
			6223: "TrueCrypt PBKDF2-HMAC-SHA512 XTS 1536 bit",
			6231: "TrueCrypt PBKDF2-HMAC-Whirlpool XTS 512 bit",
			6232: "TrueCrypt PBKDF2-HMAC-Whirlpool XTS 1024 bit",
			6233: "TrueCrypt PBKDF2-HMAC-Whirlpool XTS 1536 bit",
			6241: "TrueCrypt PBKDF2-HMAC-RIPEMD160 + boot-mode XTS 512 bit",
			6242: "TrueCrypt PBKDF2-HMAC-RIPEMD160 + boot-mode XTS 1024 bit",
			6243: "TrueCrypt PBKDF2-HMAC-RIPEMD160 + boot-mode XTS 1536 bit",
			8800: "Android FDE &lt;= 4.3",
			12900: "Android FDE (Samsung DEK",
			12200: "eCryptfs" ,
			13711: "VeraCrypt PBKDF2-HMAC-RIPEMD160 XTS 512 bit",
			13712: "VeraCrypt PBKDF2-HMAC-RIPEMD160 XTS 1024 bit",
			13713: "VeraCrypt PBKDF2-HMAC-RIPEMD160 XTS 1536 bit",
			13721: "VeraCrypt PBKDF2-HMAC-SHA512 XTS 512 bit",
			13722: "VeraCrypt PBKDF2-HMAC-SHA512 XTS 1024 bit",
			13723: "VeraCrypt PBKDF2-HMAC-SHA512 XTS 1536 bit",
			13731: "VeraCrypt PBKDF2-HMAC-Whirlpool XTS 512 bit",
			13732: "VeraCrypt PBKDF2-HMAC-Whirlpool XTS 1024 bit",
			13733: "VeraCrypt PBKDF2-HMAC-Whirlpool XTS 1536 bit",
			13741: "VeraCrypt PBKDF2-HMAC-RIPEMD160 + boot-mode XTS 512 bit",
			13742: "VeraCrypt PBKDF2-HMAC-RIPEMD160 + boot-mode XTS 1024 bit",
			13743: "VeraCrypt PBKDF2-HMAC-RIPEMD160 + boot-mode",
			13751: "VeraCrypt PBKDF2-HMAC-SHA256 XTS 512 bit",
			13752: "VeraCrypt PBKDF2-HMAC-SHA256 XTS 1024 bit",
			13753: "VeraCrypt PBKDF2-HMAC-SHA256 XTS 1536 bit",
			13761: "VeraCrypt PBKDF2-HMAC-SHA256 + boot-mode XTS 512 bit",
			13762: "VeraCrypt PBKDF2-HMAC-SHA256 + boot-mode XTS 1024 bit",
			13763: "VeraCrypt PBKDF2-HMAC-SHA256 + boot-mode",
			13771: "VeraCrypt PBKDF2-HMAC-Streebog-512 XTS 512 bit",
			13772: "VeraCrypt PBKDF2-HMAC-Streebog-512 XTS 1024 bit",
			13773: "VeraCrypt PBKDF2-HMAC-Streebog-512 XTS 1536 bit",
			14600: "LUKS",
			16700: "FileVault 2",
			18300: "Apple File System (APFS",
			9700: "MS Office &lt;= 2003 $0/$1, MD5 + RC4",
			9710: "MS Office &lt;= 2003 $0/$1, MD5 + RC4, collider #1",
			9720: "MS Office &lt;= 2003 $0/$1, MD5 + RC4, collider #2",
			9800: "MS Office &lt;= 2003 $3/$4, SHA1 + RC4",
			9810: "MS Office &lt;= 2003 $3, SHA1 + RC4, collider #1",
			9820: "MS Office &lt;= 2003 $3, SHA1 + RC4, collider #2",
			9400: "MS Office 2007",
			9500: "MS Office 2010",
			9600: "MS Office 2013",
			10400: "PDF 1.1 - 1.3 (Acrobat 2 - 4",
			10410: "PDF 1.1 - 1.3 (Acrobat 2 - 4), collider #1",
			10420: "PDF 1.1 - 1.3 (Acrobat 2 - 4), collider #2",
			10500: "PDF 1.4 - 1.6 (Acrobat 5 - 8",
			10600: "PDF 1.7 Level 3 (Acrobat 9",
			10700: "PDF 1.7 Level 8 (Acrobat 10 - 11",
			16200: "Apple Secure Notes",
			9000: "Password Safe v2",
			5200: "Password Safe v3",
			6800: "LastPass + LastPass sniffed",
			6600: "1Password, agilekeychain",
			8200: "1Password, cloudkeychain",
			11300: "Bitcoin/Litecoin wallet.dat",
			12700: "Blockchain, My Wallet",
			15200: "Blockchain, My Wallet, V2",
			16600: "Electrum Wallet (Salt-Type 1-3",
			13400: "KeePass 1 (AES/Twofish) and KeePass 2 (AES",
			15500: "JKS Java Key Store Private Keys (SHA1",
			15600: "Ethereum Wallet, PBKDF2-HMAC-SHA256",
			15700: "Ethereum Wallet, SCRYPT",
			16300: "Ethereum Pre-Sale Wallet, PBKDF2-HMAC-SHA256",
			16900: "Ansible Vault",
			18100: "TOTP (HMAC-SHA1",
			99999: "Plaintext"
		}
		return switcher.get(self.hashType,"Invalid_Hash_Type")

class Hash(models.Model):
	crackingTask = models.ForeignKey(CrackingTask, on_delete=models.CASCADE)
	hashText = models.CharField(max_length=500)
	password = models.CharField(max_length=500)
	username = models.CharField(max_length=500)

