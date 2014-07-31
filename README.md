#Anrin
Anrin is a tool intended for IT personnel who need to export log files to external companies and other third partied. Some logs (firewalls, routers and so on) contain information such as IP addresses, MAC addresses and domain names. Usually we keep this sort of information well guarded but when exporting those logs we allow other entities to view it (along with routing information and other types of sensitive data).

Anrin will be watching a folder to see new files. When a new file is added it will search for IP addresses, MAC addresses and domain named within this file. Then it will generate 'random' data to replace it. The thing about Anrin is that it will keep the basic logic behind it. 

For example;

    IP: 192.168.3.1 is trying to contact 192.168.3.4
    IP: 192.168.3.1 is trying to contact 192.168.3.5
    IP: 192.168.3.1 is trying to contact 192.168.2.3
    
Will be broken down into segments and will be replaced (for example) with:

    IP: 143.214.34.98 is trying to contact 143.214.34.132
    IP: 143.214.34.98 is trying to contact 143.214.34.15
    IP: 143.214.34.98 is trying to contact 143.214.13.132
    
The new file will be stored into the folder 'blacked' and will be assigned a random 6 chars name. In addition to the "encrypted" file there will also be a dictionary file in the same folder. This dictionary file is the "key" to the encrypted file. Do not transfer it to a side you do not trust. It will render the process useless and the original data open.
 
Please notice that this program depends on 'pyinotify' and is only a Linux library.

## GPLv3
Anrin - A Log file Censor Tool
Copyright (C) 2014 Yuval tisf Nativ

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.