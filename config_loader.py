# config_loader.py
#    auto_kyanite
#    Copyright (C) 2023  MedicBehindYou
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import configparser
def load_config(config_file='/config/config.ini'):
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        return config
    except Exception as e:
        error_message = f'Error loading config: {e}'
        print(error_message)
        return None
