#
# auto-pts - The Bluetooth PTS Automation Framework
#
# Copyright (c) 2017, Intel Corporation.
# Copyright (c) 2022, Codecoup.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#

"""VOCS test cases"""

from autopts.pybtp import btp
from autopts.client import get_unique_name
from autopts.ptsprojects.stack import get_stack
from autopts.ptsprojects.testcase import TestFunc
from autopts.ptsprojects.zephyr.vocs_wid import vocs_wid_hdl
from autopts.ptsprojects.zephyr.ztestcase import ZTestCase

def set_pixits(ptses):
    """Setup VCS profile PIXITS for workspace. Those values are used for test
    case if not updated within test case.

    PIXITS always should be updated accordingly to project and newest version of
    PTS.

    ptses -- list of PyPTS instances"""

    pts = ptses[0]

    pts.set_pixit("VOCS", "TSPX_bd_addr_iut", "DEADBEEFDEAD")
    pts.set_pixit("VOCS", "TSPX_iut_device_name_in_adv_packet_for_random_address", "")
    pts.set_pixit("VOCS", "TSPX_time_guard", "180000")
    pts.set_pixit("VOCS", "TSPX_use_implicit_send", "TRUE")
    pts.set_pixit(
        "VCS",
        "TSPX_tester_database_file",
        r"C:\Program Files\Bluetooth SIG\Bluetooth PTS\Data\SIGDatabase\PTS_PXP_db")
    pts.set_pixit("VOCS", "TSPX_mtu_size", "23")
    pts.set_pixit("VOCS", "TSPX_secure_simple_pairing_pass_key_confirmation", "FALSE")
    pts.set_pixit("VOCS", "TSPX_delete_link_key", "FALSE")
    pts.set_pixit("VOCS", "TSPX_pin_code", "0000")
    pts.set_pixit("VOCS", "TSPX_use_dynamic_pin", "FALSE")
    pts.set_pixit("VOCS", "TSPX_delete_ltk", "FALSE")
    pts.set_pixit("VOCS", "TSPX_security_enabled", "FALSE")
    pts.set_pixit("VOCS", "TSPX_iut_setup_att_over_br_edr", "FALSE")
    pts.set_pixit("VOCS", "TSPX_tester_appearance", "0000")
    pts.set_pixit("VOCS", "TSPX_Step_Size", "1")
    pts.set_pixit("VOCS", "TSPX_iut_ATT_trnasport", "ATT Bearer on LE Transport")

def test_cases(ptses):
    """Returns a list of VOCS Server test cases"""

    pts = ptses[0]

    iut_device_name = get_unique_name(pts)
    stack = get_stack()
    stack.vcs_init()

    pre_conditions = [TestFunc(btp.core_reg_svc_gap),
                      TestFunc(stack.gap_init, iut_device_name),
                      TestFunc(btp.gap_read_ctrl_info),
                      TestFunc(lambda: pts.update_pixit_param(
                            "VOCS", "TSPX_bd_addr_iut",
                            stack.gap.iut_addr_get_str())),
                      TestFunc(lambda: pts.update_pixit_param(
                          "VOCS", "TSPX_iut_use_dynamic_bd_addr",
                          "TRUE" if stack.gap.iut_addr_is_random()
                          else "FALSE")),
                      TestFunc(btp.core_reg_svc_gatt),
                      TestFunc(btp.gap_set_conn),
                      TestFunc(btp.gap_set_gendiscov),
                      TestFunc(btp.core_reg_svc_vocs),
                      TestFunc(stack.vocs_init)]

    test_case_name_list = pts.get_test_case_list('VOCS')
    tc_list = []

    for tc_name in test_case_name_list:
        instance = ZTestCase("VOCS", tc_name,
                             cmds=pre_conditions,
                             generic_wid_hdl=vocs_wid_hdl)
        tc_list.append(instance)

    return tc_list