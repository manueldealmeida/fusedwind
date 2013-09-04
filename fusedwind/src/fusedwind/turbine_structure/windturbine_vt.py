import numpy as np
from openmdao.main.api import VariableTree
from openmdao.lib.datatypes.api import Int, Float, Array, List, Str, Enum


class WindTurbineDescriptionVT(VariableTree):
    
    turbine_name = Str('FUSED-Wind turbine', desc='Wind turbine name')
    docs = Str(desc='Human readable description of wind turbine')


class RotorVT(VariableTree):

    hub_height = Float(desc='Hub height')
    nb = Int(desc='Number of blades')
    tilt_angle = Float(desc='Tilt angle')
    cone_angle = Float(desc='Cone angle')
    diameter = Float(desc='Rotor diameter')
    mass = Float(desc='Total mass')
    overhang = Float(desc='Rotor overhang')


class BladeVT(VariableTree):

    length = Float(desc='blade length')
    mass = Float(desc='blade mass')
    I_x = Float(desc='first area moment of inertia')
    I_y = Float(desc='Second area moment of inertia')
    root_chord = Float(desc='Blade root chord')
    max_chord = Float(desc='Blade maximum chord')
    tip_chord = Float(desc='Blade tip chord')
    airfoils = List(desc='List of airfoil names used on blade')


class HubVT(VariableTree):

    diameter = Float(desc='blade length')
    mass = Float(desc='blade mass')
    I_x = Float(desc='first area moment of inertia')
    I_y = Float(desc='Second area moment of inertia')
    CM = Array(np.zeros(3), desc='')


class NacelleVT(VariableTree):

    mass = Float(desc='blade mass')
    I_x = Float(desc='first area moment of inertia')
    I_y = Float(desc='Second area moment of inertia')
    CM = Array(np.zeros(3), desc='')


class GeneratorVT(VariableTree):

    mass = Float(desc='blade mass')
    I_x = Float(desc='first area moment of inertia')
    I_y = Float(desc='Second area moment of inertia')
    power = Float(desc='Generator power')
    efficiency = Float(desc='Generator efficiency')


class TransmissionVT(VariableTree):

    gear_ratio = Float(desc='Transmission gear ratio')


class TowerVT(VariableTree):

    height = Float(desc='Tower height')
    bottom_diameter = Float(desc='Tower bottom diameter')
    top_diameter = Float(desc='Tower bottom diameter')
    mass = Float(desc='Tower mass')
