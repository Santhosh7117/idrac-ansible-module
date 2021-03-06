# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import rfutils
import json
import sys
rf = rfutils.rfutils()

def get_list_of_controllers(idrac, base_uri, rf_uri):
    count = 0
    controllers = []
    response = rf.send_get_request(idrac, base_uri + rf_uri)
    rf.print_bold("status_code: %s" % response.status_code)
    if not response.status_code == 200:
        rf.print_red("Something went wrong.")
        exit(1)
    data = response.json()

    for controller in data[u'Members']:
        c = controller[u'@odata.id']
        # Only PERC? What about lower-end systems with SATA controllers only?
        # if "RAID" in c or "PERC" in c:
        controllers.append(c)
    return controllers

def get_controller_disks(idrac, base_uri, controllers):
    disks = []
    for c in controllers:
        uri = base_uri + c
        response = rf.send_get_request(idrac, uri)
        if not response.status_code == 200:
            rf.print_red("Something went wrong.")
            exit(1)
        data = response.json()
        rf.print_bold("Controller name: %s" % data[u'Name'])

        for disk in data[u'Devices']:
            print("Disk name: %s" % disk[u'Name'])
            print("Disk mfg: %s" % disk[u'Manufacturer'])
            print("Disk model: %s" % disk[u'Model'])
            print("Disk state: %s" % disk[u'Status'][u'State'])
            print("Disk health: %s\n" % disk[u'Status'][u'Health'])
            disks.append(disk)
    return disks

def main():
    # Initialize iDRAC arguments
    idrac = rf.check_args(sys)
    base_uri = "https://" + idrac['ip']
    rf_uri = "/redfish/v1/Systems/System.Embedded.1/Storage/Controllers/"

    # Get all devices
    controllers = get_list_of_controllers(idrac, base_uri, rf_uri)

    # Go through list of devices and get detailed information for each one
    disks = get_controller_disks(idrac, base_uri, controllers)

    # Uncomment if you want to see all fields returned
    # for d in disks: print(d)

if __name__ == '__main__':
    main()
