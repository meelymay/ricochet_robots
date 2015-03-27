##
# Trifacta Inc. Confidential
#
# Copyright 2015 Trifacta Inc.
# All Rights Reserved.
#
# Any use of this material is subject to the Trifacta Inc., Source License located
# in the file 'SOURCE_LICENSE.txt' which is part of this package.  All rights to
# this material and any derivative works thereof are reserved by Trifacta Inc.
#

import json
import board


class RicochetJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, board.Board):
            view = []
            for x, row in enumerate(self.board):
                for y, square in enumerate(row):
                    obj = {}
                    obj['x'] = x
                    obj['y'] = y
                    obj['hor'] = square.hor_wall
                    obj['vert'] = square.vert_wall
                    obj['robot'] = square.robot
                    view.append(obj)
            return view

        return json.JSONEncoder.default(self, obj)
