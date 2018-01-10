import os
import subprocess

from bottle import route, run, template, static_file, request
from src.config import templates


class InvalidInitialStateException(Exception):
    def __init__(self, x, y, d):
        self.msg = f'Invalid initial position ({x}, {y}, {d}): cancelling/skipping further movement instructions'


class InvalidCoordinatesException(Exception):
    def __init__(self, x, y):
        self.msg = f'Invalid out-of-the-bounds co-ordinates ({x}, {y}): cancelling/skipping further movement instructions'


class InvalidInstructiosException(Exception):
    def __init__(self, step):
        self.msg = f'Invalid instructions cancelling/skipping further movement instructions'


class MarsRover(object):

    def __init__(self, x, y, direction, bnd_x, bnd_y):
        self.move_dict = {'N': self._move_north,
                          'S': self._move_south,
                          'E': self._move_east,
                          'W': self._move_west}
        if x < 0 or y < 0 or x > bnd_x or y > bnd_y or direction not in self.move_dict.keys():
            raise InvalidCoordinatesException(x, y, direction)
        self.x = x
        self.y = y
        self.bnd_x = bnd_x
        self.bnd_y = bnd_y
        self.direction = direction

        self.dir_dict = {'N': {'L': 'W', 'R': 'E'},
                         'S': {'L': 'E', 'R': 'W'},
                         'E': {'L': 'N', 'R': 'S'},
                         'W': {'L': 'S', 'R': 'N'}}

    def change_direction(self, step):
        self.direction = self.dir_dict[self.direction][step]

    def move(self, steps):
        for step in steps:
            if step == 'M':
                self.move_dict[self.direction]()
            elif step in ('L', 'R'):
                self.change_direction(step)
            else:
                raise InvalidInstructiosException(step)

    def _move_east(self):
        if self.x+1 <= self.bnd_x:
            self.x = self.x+1
        else:
            raise InvalidCoordinatesException(self.x+1, self.y)

    def _move_west(self):
        if self.x-1 >= 0:
            self.x = self.x-1
        else:
            raise InvalidCoordinatesException(self.x-1, self.y)

    def _move_north(self):
        if self.y+1 <= self.bnd_y:
            self.y = self.y+1
        else:
            raise InvalidCoordinatesException(self.x, self.y+1)

    def _move_south(self):
        if self.y-1 >=0:
            self.y = self.y-1
        else:
            raise InvalidCoordinatesException(self.x, self.y-1)


def main(test_data):
    print(test_data)
    print(os.getcwd())
    output = '\n'
    if not test_data:
        with open('src/test_data.txt', mode='r') as test_file:
            test_file_lines = test_file.readlines()
    else:
        test_file_lines = test_data.split('\n')
    bnd = test_file_lines.pop(0)
    try:
        bnd_x, bnd_y = bnd.strip().split()
    except ValueError:
        output += f'''Invalid boundary co-ordinates: ({bnd.strip()}) '''
        return output
    n_rovers = len(test_file_lines)//2
    for i in range(n_rovers):
        state = test_file_lines.pop(0)
        steps = test_file_lines.pop(0).strip()
        try:
            x, y, direction = state.strip().split()
            rover = MarsRover(int(x), int(y), direction, int(bnd_x), int(bnd_y))

            rover.move(steps)
            output += str(rover.x) + ' ' + str(rover.y) + ' ' + rover.direction + '\n'
        except ValueError:
            output += f'''Invalid initial state: ({state.strip()}) \n'''
        except InvalidCoordinatesException as ex:
            output += ex.msg + '  -  ' + str(rover.x) + ' ' + str(rover.y) + ' ' + rover.direction + '\n'
        except InvalidInstructiosException as ex:
            output += ex.msg + ' (' + steps + ')' + '  -  ' + str(rover.x) + ' ' + str(rover.y) + ' ' + rover.direction + '\n'

    return(output)
    print('==========')


@route('/<filename>')
def server_static(filename):
    cwd = os.getcwd()
    root = cwd + '\src\config'
    print(root, static_file(filename, root=root))
    return static_file(filename, root=root)


@route('/')
@route('/test/')
def search():
    tpl = templates.tpl_home
    return template(tpl)


@route('/test/output', method="POST")
def formhandler():
    test_data = request.forms.get('test_data')
    ppl = main(test_data)
    tpl = templates.tpl_start + templates.tpl_form_cmp.format(res_tag=ppl) \
          + templates.tpl_end
    return tpl



if __name__ == '__main__':
    if os.path.isfile('/sys/hypervisor/uuid') \
            and 'ec2' in subprocess.check_output(['head' '-1' '/sys/hypervisor/uuid']).decode():
        host = subprocess.check_output(['curl' 'http://169.254.169.254/latest/meta-data/public-hostname']).decode()
        run(server='auto', host=host, port=8080)
    else:
        run()
