import math
import pytest
from src.osdag.utils.common.is800_2025 import IS800_2025


def test_table2_outstanding_element():
    assert IS800_2025.Table2_i_outstanding_element(80, 10, 250)[0] == 'Plastic'
    assert IS800_2025.Table2_i_outstanding_element(95, 10, 250)[0] == 'Compact'
    assert IS800_2025.Table2_i_outstanding_element(130, 10, 250)[0] == 'Semi-Compact'
    assert IS800_2025.Table2_i_outstanding_element(140, 10, 250)[0] == 'Slender'


def test_table2_web_classification():
    assert IS800_2025.Table2_ii_web_I_channel_H_box(650, 10, 250)[0] == 'Plastic'
    assert IS800_2025.Table2_ii_web_I_channel_H_box(750, 10, 250)[0] == 'Compact'
    assert IS800_2025.Table2_ii_web_I_channel_H_box(1150, 10, 250)[0] == 'Semi-Compact'
    assert IS800_2025.Table2_ii_web_I_channel_H_box(1250, 10, 250)[0] == 'Slender'
    assert IS800_2025.Table2_ii_web_I_channel_H_box(300, 10, 250, 'Axial compression')[0] == 'Plastic'
    assert IS800_2025.Table2_ii_web_I_channel_H_box(350, 10, 250, 'Axial compression')[0] == 'Compact'
    assert IS800_2025.Table2_ii_web_I_channel_H_box(400, 10, 250, 'Axial compression')[0] == 'Semi-Compact'
    assert IS800_2025.Table2_ii_web_I_channel_H_box(420, 10, 250, 'Axial compression')[0] == 'Slender'


def test_table2_circular_hollow_tube():
    assert IS800_2025.Table2_vi_circular_hollow_tube(450, 10, 250, 'Moment')[0] == 'Plastic'
    assert IS800_2025.Table2_vi_circular_hollow_tube(600, 10, 250, 'Moment')[0] == 'Compact'
    assert IS800_2025.Table2_vi_circular_hollow_tube(800, 10, 250, 'Moment')[0] == 'Semi-Compact'
    assert IS800_2025.Table2_vi_circular_hollow_tube(900, 10, 250, 'Moment')[0] == 'Slender'
    assert IS800_2025.Table2_vi_circular_hollow_tube(860, 10, 250, 'Axial Compression')[0] == 'Semi-Compact'


def test_max_slenderness_ratio():
    assert IS800_2025.cl_10_9_1_max_slenderness_ratio(1) == 180
    assert IS800_2025.cl_10_9_1_max_slenderness_ratio(3) == 250
    assert IS800_2025.cl_10_9_1_max_slenderness_ratio(6) == 400


def test_column_buckling_against_table_8a_and_9a():
    res = IS800_2025.cl_14_1_2_1_design_compressive_stress(250.0, 100.0, 'a0')
    assert math.isclose(res['chi'], 0.629, abs_tol=0.002)
    assert math.isclose(res['f_cd'], 143.0, abs_tol=0.5)


def test_buckling_class_high_strength_steel():
    assert IS800_2025.cl_14_1_2_2_buckling_class_of_cross_sections(200, 400, 20, f_y=250) == {'z-z': 'a', 'y-y': 'b'}
    assert IS800_2025.cl_14_1_2_2_buckling_class_of_cross_sections(200, 400, 20, f_y=450) == {'z-z': 'a0', 'y-y': 'a'}


def test_column_base_bearing_strength():
    assert math.isclose(IS800_2025.cl_14_4_1_bearing_strength_concrete('M25', 40000, 10000), 22.5)
    assert math.isclose(IS800_2025.cl_14_4_1_bearing_strength_concrete('M25', 10000, 10000), 11.25)


def test_single_angle_strut_one_leg():
    res = IS800_2025.cl_14_5_1_2_single_angle_strut_one_leg(
        l_aa=2000, r_aa=20, b1=65, b2=65, t=6, f_y=250, bolt_no=2, fixity='Fixed'
    )
    assert res['f_cde'] > 0
    assert 0 < res['chi_aa'] <= 1.0


def test_ltb_alpha_LT_and_chi_LT():
    alpha_lt = IS800_2025.cl_15_2_2_alpha_LT('Rolled unequal I/H', h=400, b_min=150)
    assert alpha_lt == 0.34
    chi_lt, _ = IS800_2025.cl_15_2_2_LTB_stress_reduction_factor(0.8, 0.9, alpha_lt, f_m=1.05)
    assert 0 < chi_lt <= 1.0


def test_connections_bolt_and_weld():
    assert IS800_2025.cl_17_2_1_bolt_hole_size(20, 'Standard') == 22.0
    assert math.isclose(IS800_2025.cl_17_5_7_1_1_fillet_weld_design_stress([410, 410], 'Shop'), 410 / (math.sqrt(3) * 1.25))
