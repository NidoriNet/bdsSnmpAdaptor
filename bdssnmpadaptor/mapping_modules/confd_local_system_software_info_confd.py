# -*- coding: utf-8 -*-
#
# This file is part of bdsSnmpAdaptor software.
#
# Copyright (C) 2017-2019, RtBrick Inc
# License: BSD License 2.0
#

from bdssnmpadaptor import mapping_functions


class ConfdLocalSystemSoftwareInfoConfd(object):
    """Local system software information
    """

    @classmethod
    def setOids(cls, bdsJsonResponseDict, targetOidDb,
                tableSequenceList, birthday):

        swString = mapping_functions.stringFromSoftwareInfo(bdsJsonResponseDict)

        with targetOidDb.module(__name__) as add:

            #add('IF-MIB', 'ifDescr', 1, value=swString)
            add('SNMPv2-MIB', 'sysDescr', 1, value=swString)

            # targetOidDb.deleteOidsWithPrefix(oidSegment)  #delete existing TableOids

            # for index,bdsJsonObject in enumerate(bdsJsonResponseDict['objects"]):
            #     #indexString = bdsJsonObject["attribute"]["library"]
            #     #indexCharList = [str(ord(c)) for c in indexString]
            #     #index = str(len(indexCharList)) + "." + ".".join(indexCharList)  # FIXME add description
            #
            #     add('HOST-RESOURCES-MIB', 'hrSWRunIndex', index, value=index)
            #
            #     add('HOST-RESOURCES-MIB', 'hrSWRunName', index,
            #          value=bdsJsonObject["attribute"]["commit_id"])

            #     add('HOST-RESOURCES-MIB', 'commitDate', index,
            #         value=bdsJsonObject["attribute"]["commit_date"])

            #     add('HOST-RESOURCES-MIB', 'packageDate', index,
            #         value=bdsJsonObject["attribute"]["package_date"])

            #     add('HOST-RESOURCES-MIB', 'vcCheckout', index,
            #         value=bdsJsonObject["attribute"]["vc_checkout"])

            #     add('HOST-RESOURCES-MIB', 'branch', index,
            #         value=bdsJsonObject["attribute"]["branch"])

            #     add('HOST-RESOURCES-MIB', 'libraryVersion', index,
            #         value=bdsJsonObject["attribute"]["version"])

            #     add('HOST-RESOURCES-MIB', 'sourcePath', index,
            #         value=bdsJsonObject["attribute"]["source_path"])

            # # in addition the SW Info Flag is set by
            # # creating an abbreviated string over all modules
