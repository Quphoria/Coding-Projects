======
Kulka
======

A python client for sphero

**EXAMPLES:**

.. code-block:: python

    from kulka import Kulka
    
    with Kulka('01:02:03:04:05:06') as kulka:
        kulka.set_inactivity_timeout(3600)
        kulka.set_rgb(0xFF, 0, 0)

.. code-block:: python

    from kulka import Kulka
    from random import randint
    
    with Kulka('01:02:03:04:05:06') as kulka:
        kulka.set_inactivity_timeout(3600)
        kulka.roll(randint(0, 255), randint(0, 359))

**INSTALLATION:**

    pip install kulka

**LICENSE:**

  Kulka is free software; you can redistribute it and/or modify it under the
  terms of the GNU General Public License as published by the Free Software
  Foundation; either version 2 of the License, or (at your option) any later
  version.
  
  Kulka is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
  A PARTICULAR PURPOSE. See the GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License along with
  Kulka; if not, write to the Free Software Foundation, Inc., 51 Franklin St,
  Fifth Floor, Boston, MA  02110-1301  USA
