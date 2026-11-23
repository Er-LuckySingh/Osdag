"""Module for Indian Standard, Draft IS 800 : 2025 (Fourth Revision)
Doc: CED 07 (27869) WC (April 2025)

Migrated from is800_2007.py following Osdag coding conventions.
"""
import math

try:
    from ...Common import *
except ImportError:
    KEY_Plastic = 'Plastic'
    KEY_Compact = 'Compact'
    KEY_SemiCompact = 'Semi-Compact'
    KEY_DP_FAB_SHOP = 'Shop'
    KEY_DP_FAB_FIELD = 'Field'


class IS800_2025(object):
    """Perform structural steel design calculations as per Draft IS 800:2025."""

    # SECTION 9: MATERIALS (Cl. 9.2.4.1)
    STEEL_DENSITY = 7850.0         # kg/m^3
    MODULUS_OF_ELASTICITY = 2.0e5  # MPa (N/mm^2)
    POISSON_RATIO = 0.3
    MODULUS_OF_RIGIDITY = 0.769e5  # MPa (N/mm^2)
    THERMAL_EXPANSION = 12e-6      # /deg C

    # SECTION 10: GENERAL DESIGN REQUIREMENTS (Cl. 10.8, Table 2)
    @staticmethod
    def Table2_i_outstanding_element(width, thickness, f_y):
        """Classify an outstanding compression element under uniform compression
        as per Table 2, Sl. No. (i) of Draft IS 800:2025.
        """
        epsilon = math.sqrt(250.0 / f_y)
        ratio = width / thickness
        if ratio <= 8.7 * epsilon:
            section_class = KEY_Plastic
        elif ratio <= 9.7 * epsilon:
            section_class = KEY_Compact
        elif ratio <= 13.6 * epsilon:
            section_class = KEY_SemiCompact
        else:
            section_class = 'Slender'
        return [section_class, ratio]

    @staticmethod
    def Table2_ii_web_I_channel_H_box(depth, thickness, f_y,
                                      classification_type='Neutral axis at mid-depth'):
        """Classify the web of an I, Channel, H, or Box section as per Table 2,
        Sl. No. (ii) of Draft IS 800:2025.
        """
        epsilon = math.sqrt(250.0 / f_y)
        ratio = depth / thickness
        if classification_type == 'Neutral axis at mid-depth':
            if ratio <= 70.0 * epsilon:
                section_class = KEY_Plastic
            elif ratio <= 80.0 * epsilon:
                section_class = KEY_Compact
            elif ratio <= 120.0 * epsilon:
                section_class = KEY_SemiCompact
            else:
                section_class = 'Slender'
        elif classification_type == 'Axial compression':
            if ratio <= 32.0 * epsilon:
                section_class = KEY_Plastic
            elif ratio <= 36.8 * epsilon:
                section_class = KEY_Compact
            elif ratio <= 40.7 * epsilon:
                section_class = KEY_SemiCompact
            else:
                section_class = 'Slender'
        else:
            raise ValueError(f"Unsupported classification_type: {classification_type}")
        return [section_class, ratio]

    @staticmethod
    def Table2_iii_angle_bending(width, depth, thickness, f_y):
        """Classify an angle section subjected to compression due to bending
        as per Table 2, Sl. No. (iii) of Draft IS 800:2025.
        """
        epsilon = math.sqrt(250.0 / f_y)
        b_t = width / thickness
        d_t = depth / thickness
        if b_t <= 8.7 * epsilon and d_t <= 8.7 * epsilon:
            section_class = KEY_Plastic
        elif b_t <= 9.7 * epsilon and d_t <= 9.7 * epsilon:
            section_class = KEY_Compact
        elif b_t <= 14.5 * epsilon and d_t <= 14.5 * epsilon:
            section_class = KEY_SemiCompact
        else:
            section_class = 'Slender'
        return [section_class, b_t, d_t]

    @staticmethod
    def Table2_iv_angle_axial_compression(width, depth, thickness, f_y):
        """Classify a single angle or separated double angle under axial
        compression as per Table 2, Sl. No. (iv) of Draft IS 800:2025.
        """
        epsilon = math.sqrt(250.0 / f_y)
        b_t = width / thickness
        d_t = depth / thickness
        bd_t = (width + depth) / thickness
        if b_t <= 14.5 * epsilon and d_t <= 14.5 * epsilon and bd_t <= 22.3 * epsilon:
            section_class = KEY_SemiCompact
        else:
            section_class = 'Slender'
        return [section_class, b_t, d_t, bd_t]

    @staticmethod
    def Table2_vi_circular_hollow_tube(outer_diameter, tube_thickness, f_y,
                                       load_type='Axial Compression'):
        """Classify a circular hollow tube (including welded tube) as per
        Table 2, Sl. No. (vi) of Draft IS 800:2025.
        """
        epsilon = math.sqrt(250.0 / f_y)
        ratio = outer_diameter / tube_thickness
        if load_type.lower() == 'axial compression':
            section_class = KEY_SemiCompact if ratio <= 86.0 * (epsilon ** 2) else 'Slender'
        elif load_type.lower() == 'moment':
            if ratio <= 47.0 * (epsilon ** 2):
                section_class = KEY_Plastic
            elif ratio <= 66.0 * (epsilon ** 2):
                section_class = KEY_Compact
            elif ratio <= 85.0 * (epsilon ** 2):
                section_class = KEY_SemiCompact
            else:
                section_class = 'Slender'
        else:
            raise ValueError(f"Unsupported load_type: {load_type}")
        return [section_class, ratio]

    @staticmethod
    def cl_10_9_1_max_slenderness_ratio(member_type=1):
        """Return maximum effective slenderness ratio (KL/r) per Table 3 (Cl. 10.9.1)."""
        limits = {1: 180, 2: 180, 3: 250, 4: 300, 5: 350, 6: 400}
        if member_type not in limits:
            raise ValueError("member_type must be an integer between 1 and 6.")
        return limits[member_type]

    # SECTION 12: LIMIT STATE DESIGN (Cl. 12.4.1, Table 5)
    cl_12_4_1_Table_5 = {
        "gamma_m0": {'yielding': 1.10, 'buckling': 1.10},
        "gamma_m1": {'ultimate_stress': 1.25},
        "gamma_mf": {KEY_DP_FAB_SHOP: 1.25, KEY_DP_FAB_FIELD: 1.25},
        "gamma_mb": {KEY_DP_FAB_SHOP: 1.25, KEY_DP_FAB_FIELD: 1.25},
        "gamma_mr": {KEY_DP_FAB_SHOP: 1.25, KEY_DP_FAB_FIELD: 1.25},
        "gamma_mw": {KEY_DP_FAB_SHOP: 1.25, KEY_DP_FAB_FIELD: 1.50}
    }

    # SECTION 13: DESIGN OF TENSION MEMBERS
    @staticmethod
    def cl_13_2_tension_yielding_strength(A_g, f_y):
        """Design strength due to yielding of gross section (T_dg), Cl. 13.2."""
        gamma_m0 = IS800_2025.cl_12_4_1_Table_5["gamma_m0"]['yielding']
        return A_g * f_y / gamma_m0

    @staticmethod
    def cl_13_3_1_tension_rupture_strength(A_n, f_u):
        """Design strength due to rupture of net section (T_dn), Cl. 13.3.1."""
        gamma_m1 = IS800_2025.cl_12_4_1_Table_5["gamma_m1"]['ultimate_stress']
        return 0.9 * A_n * f_u / gamma_m1

    @staticmethod
    def cl_13_4_1_block_shear_strength(A_vg, A_vn, A_tg, A_tn, f_u, f_y):
        """Block shear strength of bolted connections (T_db), Cl. 13.4.1."""
        gamma_m0 = IS800_2025.cl_12_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2025.cl_12_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_db1 = (A_vg * f_y / (math.sqrt(3) * gamma_m0)) + (0.9 * A_tn * f_u / gamma_m1)
        T_db2 = (0.9 * A_vn * f_u / (math.sqrt(3) * gamma_m1)) + (A_tg * f_y / gamma_m0)
        return min(T_db1, T_db2)

    # SECTION 14: DESIGN OF COMPRESSION MEMBERS
    @staticmethod
    def cl_14_1_2_imperfection_factor(buckling_class):
        """Imperfection factor alpha per Table 7 (includes class 'a0' = 0.13)."""
        table_7 = {'a0': 0.13, 'a': 0.21, 'b': 0.34, 'c': 0.49, 'd': 0.76}
        if buckling_class not in table_7:
            raise ValueError(f"Invalid buckling_class '{buckling_class}'.")
        return table_7[buckling_class]

    @staticmethod
    def cl_14_1_2_1_design_compressive_stress(f_y, effective_slenderness_ratio,
                                              buckling_class,
                                              modulus_of_elasticity=2.0e5):
        """Flexural buckling reduction factor (chi) and design compressive stress
        (f_cd) per Cl. 14.1.2.1. Uses sqrt(phi^2 - lambda^2) matching Tables 8 & 9.
        """
        gamma_m0 = IS800_2025.cl_12_4_1_Table_5["gamma_m0"]['buckling']
        alpha = IS800_2025.cl_14_1_2_imperfection_factor(buckling_class)
        f_cr = (math.pi ** 2 * modulus_of_elasticity) / (effective_slenderness_ratio ** 2)
        lam = math.sqrt(f_y / f_cr)
        phi = 0.5 * (1.0 + alpha * (lam - 0.2) + lam ** 2)
        chi = min(1.0 / (phi + math.sqrt(phi ** 2 - lam ** 2)), 1.0)
        f_cd = min(chi * f_y / gamma_m0, f_y / gamma_m0)
        return {'f_cr': f_cr, 'lambda': lam, 'phi': phi, 'chi': chi, '

mkdir -p src/osdag/utils/common tests

cat << 'EOF' > src/osdag/utils/common/is800_2025.py
"""Module for Indian Standard, Draft IS 800 : 2025 (Fourth Revision)
Doc: CED 07 (27869) WC (April 2025)

Migrated from is800_2007.py following Osdag coding conventions.
"""
import math

try:
    from ...Common import *
except ImportError:
    KEY_Plastic = 'Plastic'
    KEY_Compact = 'Compact'
    KEY_SemiCompact = 'Semi-Compact'
    KEY_DP_FAB_SHOP = 'Shop'
    KEY_DP_FAB_FIELD = 'Field'


class IS800_2025(object):
    """Perform structural steel design calculations as per Draft IS 800:2025."""

    # SECTION 9: MATERIALS (Cl. 9.2.4.1)
    STEEL_DENSITY = 7850.0         # kg/m^3
    MODULUS_OF_ELASTICITY = 2.0e5  # MPa (N/mm^2)
    POISSON_RATIO = 0.3
    MODULUS_OF_RIGIDITY = 0.769e5  # MPa (N/mm^2)
    THERMAL_EXPANSION = 12e-6      # /deg C

    # SECTION 10: GENERAL DESIGN REQUIREMENTS (Cl. 10.8, Table 2)
    @staticmethod
    def Table2_i_outstanding_element(width, thickness, f_y):
        """Classify an outstanding compression element under uniform compression
        as per Table 2, Sl. No. (i) of Draft IS 800:2025.
        """
        epsilon = math.sqrt(250.0 / f_y)
        ratio = width / thickness
        if ratio <= 8.7 * epsilon:
            section_class = KEY_Plastic
        elif ratio <= 9.7 * epsilon:
            section_class = KEY_Compact
        elif ratio <= 13.6 * epsilon:
            section_class = KEY_SemiCompact
        else:
            section_class = 'Slender'
        return [section_class, ratio]

    @staticmethod
    def Table2_ii_web_I_channel_H_box(depth, thickness, f_y,
                                      classification_type='Neutral axis at mid-depth'):
        """Classify the web of an I, Channel, H, or Box section as per Table 2,
        Sl. No. (ii) of Draft IS 800:2025.
        """
        epsilon = math.sqrt(250.0 / f_y)
        ratio = depth / thickness
        if classification_type == 'Neutral axis at mid-depth':
            if ratio <= 70.0 * epsilon:
                section_class = KEY_Plastic
            elif ratio <= 80.0 * epsilon:
                section_class = KEY_Compact
            elif ratio <= 120.0 * epsilon:
                section_class = KEY_SemiCompact
            else:
                section_class = 'Slender'
        elif classification_type == 'Axial compression':
            if ratio <= 32.0 * epsilon:
                section_class = KEY_Plastic
            elif ratio <= 36.8 * epsilon:
                section_class = KEY_Compact
            elif ratio <= 40.7 * epsilon:
                section_class = KEY_SemiCompact
            else:
                section_class = 'Slender'
        else:
            raise ValueError(f"Unsupported classification_type: {classification_type}")
        return [section_class, ratio]

    @staticmethod
    def Table2_iii_angle_bending(width, depth, thickness, f_y):
        """Classify an angle section subjected to compression due to bending
        as per Table 2, Sl. No. (iii) of Draft IS 800:2025.
        """
        epsilon = math.sqrt(250.0 / f_y)
        b_t = width / thickness
        d_t = depth / thickness
        if b_t <= 8.7 * epsilon and d_t <= 8.7 * epsilon:
            section_class = KEY_Plastic
        elif b_t <= 9.7 * epsilon and d_t <= 9.7 * epsilon:
            section_class = KEY_Compact
        elif b_t <= 14.5 * epsilon and d_t <= 14.5 * epsilon:
            section_class = KEY_SemiCompact
        else:
            section_class = 'Slender'
        return [section_class, b_t, d_t]

    @staticmethod
    def Table2_iv_angle_axial_compression(width, depth, thickness, f_y):
        """Classify a single angle or separated double angle under axial
        compression as per Table 2, Sl. No. (iv) of Draft IS 800:2025.
        """
        epsilon = math.sqrt(250.0 / f_y)
        b_t = width / thickness
        d_t = depth / thickness
        bd_t = (width + depth) / thickness
        if b_t <= 14.5 * epsilon and d_t <= 14.5 * epsilon and bd_t <= 22.3 * epsilon:
            section_class = KEY_SemiCompact
        else:
            section_class = 'Slender'
        return [section_class, b_t, d_t, bd_t]

    @staticmethod
    def Table2_vi_circular_hollow_tube(outer_diameter, tube_thickness, f_y,
                                       load_type='Axial Compression'):
        """Classify a circular hollow tube (including welded tube) as per
        Table 2, Sl. No. (vi) of Draft IS 800:2025.
        """
        epsilon = math.sqrt(250.0 / f_y)
        ratio = outer_diameter / tube_thickness
        if load_type.lower() == 'axial compression':
            section_class = KEY_SemiCompact if ratio <= 86.0 * (epsilon ** 2) else 'Slender'
        elif load_type.lower() == 'moment':
            if ratio <= 47.0 * (epsilon ** 2):
                section_class = KEY_Plastic
            elif ratio <= 66.0 * (epsilon ** 2):
                section_class = KEY_Compact
            elif ratio <= 85.0 * (epsilon ** 2):
                section_class = KEY_SemiCompact
            else:
                section_class = 'Slender'
        else:
            raise ValueError(f"Unsupported load_type: {load_type}")
        return [section_class, ratio]

    @staticmethod
    def cl_10_9_1_max_slenderness_ratio(member_type=1):
        """Return maximum effective slenderness ratio (KL/r) per Table 3 (Cl. 10.9.1)."""
        limits = {1: 180, 2: 180, 3: 250, 4: 300, 5: 350, 6: 400}
        if member_type not in limits:
            raise ValueError("member_type must be an integer between 1 and 6.")
        return limits[member_type]

    # SECTION 12: LIMIT STATE DESIGN (Cl. 12.4.1, Table 5)
    cl_12_4_1_Table_5 = {
        "gamma_m0": {'yielding': 1.10, 'buckling': 1.10},
        "gamma_m1": {'ultimate_stress': 1.25},
        "gamma_mf": {KEY_DP_FAB_SHOP: 1.25, KEY_DP_FAB_FIELD: 1.25},
        "gamma_mb": {KEY_DP_FAB_SHOP: 1.25, KEY_DP_FAB_FIELD: 1.25},
        "gamma_mr": {KEY_DP_FAB_SHOP: 1.25, KEY_DP_FAB_FIELD: 1.25},
        "gamma_mw": {KEY_DP_FAB_SHOP: 1.25, KEY_DP_FAB_FIELD: 1.50}
    }

    # SECTION 13: DESIGN OF TENSION MEMBERS
    @staticmethod
    def cl_13_2_tension_yielding_strength(A_g, f_y):
        """Design strength due to yielding of gross section (T_dg), Cl. 13.2."""
        gamma_m0 = IS800_2025.cl_12_4_1_Table_5["gamma_m0"]['yielding']
        return A_g * f_y / gamma_m0

    @staticmethod
    def cl_13_3_1_tension_rupture_strength(A_n, f_u):
        """Design strength due to rupture of net section (T_dn), Cl. 13.3.1."""
        gamma_m1 = IS800_2025.cl_12_4_1_Table_5["gamma_m1"]['ultimate_stress']
        return 0.9 * A_n * f_u / gamma_m1

    @staticmethod
    def cl_13_4_1_block_shear_strength(A_vg, A_vn, A_tg, A_tn, f_u, f_y):
        """Block shear strength of bolted connections (T_db), Cl. 13.4.1."""
        gamma_m0 = IS800_2025.cl_12_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2025.cl_12_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_db1 = (A_vg * f_y / (math.sqrt(3) * gamma_m0)) + (0.9 * A_tn * f_u / gamma_m1)
        T_db2 = (0.9 * A_vn * f_u / (math.sqrt(3) * gamma_m1)) + (A_tg * f_y / gamma_m0)
        return min(T_db1, T_db2)

    # SECTION 14: DESIGN OF COMPRESSION MEMBERS
    @staticmethod
    def cl_14_1_2_imperfection_factor(buckling_class):
        """Imperfection factor alpha per Table 7 (includes class 'a0' = 0.13)."""
        table_7 = {'a0': 0.13, 'a': 0.21, 'b': 0.34, 'c': 0.49, 'd': 0.76}
        if buckling_class not in table_7:
            raise ValueError(f"Invalid buckling_class '{buckling_class}'.")
        return table_7[buckling_class]

    @staticmethod
    def cl_14_1_2_1_design_compressive_stress(f_y, effective_slenderness_ratio,
                                              buckling_class,
                                              modulus_of_elasticity=2.0e5):
        """Flexural buckling reduction factor (chi) and design compressive stress
        (f_cd) per Cl. 14.1.2.1. Uses sqrt(phi^2 - lambda^2) matching Tables 8 & 9.
        """
        gamma_m0 = IS800_2025.cl_12_4_1_Table_5["gamma_m0"]['buckling']
        alpha = IS800_2025.cl_14_1_2_imperfection_factor(buckling_class)
        f_cr = (math.pi ** 2 * modulus_of_elasticity) / (effective_slenderness_ratio ** 2)
        lam = math.sqrt(f_y / f_cr)
        phi = 0.5 * (1.0 + alpha * (lam - 0.2) + lam ** 2)
        chi = min(1.0 / (phi + math.sqrt(phi ** 2 - lam ** 2)), 1.0)
        f_cd = min(chi * f_y / gamma_m0, f_y / gamma_m0)
        return {'f_cr': f_cr, 'lambda': lam, 'phi': phi, 'chi': chi, 'f_cd': f_cd}

    @staticmethod
    def cl_14_1_2_2_buckling_class_of_cross_sections(b_f, h, t_f, f_y=250.0,
                                                     cross_section='Rolled I-sections',
                                                     section_type='Hot rolled'):
        """Buckling class about z-z and y-y axes per Table 10 (f_y <= 420 vs > 420 MPa)."""
        high_strength = f_y > 420.0
        if cross_section == 'Rolled I-sections':
            if h / b_f > 1.2:
                if t_f <= 40:
                    return {'z-z': 'a0', 'y-y': 'a'} if high_strength else {'z-z': 'a', 'y-y': 'b'}
                elif t_f <= 100:
                    return {'z-z': 'a', 'y-y': 'b'} if high_strength else {'z-z': 'b', 'y-y': 'c'}
                return {'z-z': 'd', 'y-y': 'd'}
            if t_f <= 100:
                return {'z-z': 'a', 'y-y': 'a'} if high_strength else {'z-z': 'b', 'y-y': 'c'}
            return {'z-z': 'c', 'y-y': 'c'} if high_strength else {'z-z': 'd', 'y-y': 'd'}
        elif cross_section == 'Welded I-section':
            return {'z-z': 'b', 'y-y': 'c'} if t_f <= 40 else {'z-z': 'c', 'y-y': 'd'}
        elif cross_section == 'Hollow Section':
            if section_type == 'Hot rolled':
                cls = 'a0' if high_strength else 'a'
                return {'z-z': cls, 'y-y': cls}
            cls = 'c' if high_strength else 'b'
            return {'z-z': cls, 'y-y': cls}
        elif cross_section in ('Channel, Angle, T, Solid', 'Built-up Member'):
            return {'z-z': 'c', 'y-y': 'c'}
        raise ValueError(f"Unsupported cross_section: {cross_section}")

    @staticmethod
    def cl_14_4_1_bearing_strength_concrete(concrete_grade, A_1=1.0, A_2=1.0):
        """Maximum bearing strength of concrete pedestal per Cl. 14.4.1."""
        f_ck_map = {
            'M10': 10, 'M15': 15, 'M20': 20, 'M25': 25, 'M30': 30,
            'M35': 35, 'M40': 40, 'M45': 45, 'M50': 50, 'M55': 55, 'M60': 60
        }
        f_ck = f_ck_map[str(concrete_grade)]
        return min(0.45 * f_ck * math.sqrt(A_1 / A_2), 0.9 * f_ck)

    @staticmethod
    def cl_14_5_1_2_single_angle_strut_one_leg(l_aa, r_aa, b1, b2, t, f_y,
                                               bolt_no=2, fixity='Fixed',
                                               modulus_of_elasticity=2.0e5):
        """Design compressive stress (f_cde) for single angle strut loaded
        through one leg per Cl. 14.5.1.2 and Table 12.
        """
        gamma_m0 = IS800_2025.cl_12_4_1_Table_5["gamma_m0"]['buckling']
        epsilon = math.sqrt(250.0 / f_y)
        denom = epsilon * math.sqrt((math.pi ** 2 * modulus_of_elasticity) / 250.0)
        lambda_aa = (l_aa / r_aa) / denom
        lambda_phi = ((b1 + b2) / (2.0 * t)) / denom
        alpha_b = IS800_2025.cl_14_1_2_imperfection_factor('b')
        phi_aa = 0.5 * (1.0 + alpha_b * (lambda_aa - 0.2) + lambda_aa ** 2)
        chi_aa = min(1.0 / (phi_aa + math.sqrt(phi_aa ** 2 - lambda_aa ** 2)), 1.0)
        table_12 = {
            'multi': {'Fixed': (0.798, 0.563, -2.072), 'Hinged': (0.401, 0.420, -1.040)},
            'single': {'Fixed': (0.418, 0.547, -1.400), 'Hinged': (0.374, 0.415, -2.072)}
        }
        conn_key = 'multi' if bolt_no >= 2 else 'single'
        if fixity in ('Fixed', 'Hinged'):
            k1, k2, k3 = table_12[conn_key][fixity]
            K_f = k1 + k2 * lambda_aa + k3 * lambda_phi
        elif fixity == 'Partial':
            k1_f, k2_f, k3_f = table_12[conn_key]['Fixed']
            k1_h, k2_h, k3_h = table_12[conn_key]['Hinged']
            K_f = 0.5 * ((k1_f + k2_f * lambda_aa + k3_f * lambda_phi) +
                         (k1_h + k2_h * lambda_aa + k3_h * lambda_phi))
        else:
            raise ValueError(f"Invalid fixity: {fixity}")
        f_cde = K_f * chi_aa * f_y / gamma_m0
        return {'f_cde': f_cde, 'K_f': K_f, 'chi_aa': chi_aa,
                'lambda_aa': lambda_aa, 'lambda_phi': lambda_phi}

    # SECTION 15: DESIGN OF MEMBERS SUBJECTED TO BENDING
    @staticmethod
    def cl_15_2_2_alpha_LT(cross_section, h, b_min, t_f=None, Z_ez=None, Z_ey=None):
        """LTB imperfection parameter alpha_LT per Table 13 (Cl. 15.2.2)."""
        if cross_section == 'Rolled I/H':
            ratio_term = math.sqrt(Z_ez / Z_ey)
            if (h / b_min > 1.2) and (t_f is not None and t_f > 40.0):
                return min(0.16 * ratio_term, 0.49)
            return min(0.12 * ratio_term, 0.34)
        elif cross_section == 'Welded I':
            return min(0.12 * math.sqrt(Z_ez / Z_ey), 0.34)
        elif cross_section == 'Rolled unequal I/H':
            return 0.21 if (h / b_min <= 2.0) else 0.34
        elif cross_section == 'Welded unequal I':
            return 0.49 if (h / b_min <= 2.0) else 0.76
        elif cross_section == 'Other rolled':
            return 0.76
        raise ValueError(f"Unsupported cross_section: {cross_section}")

    @staticmethod
    def cl_15_2_2_LTB_stress_reduction_factor(lambda_LT, lambda_y, alpha_LT, f_m=1.0):
        """Bending stress reduction factor chi_LT per Cl. 15.2.2."""
        if lambda_LT < 0.4:
            return 1.0, 0.5
        phi_LT = 0.5 * (
            1.0 + f_m * ((lambda_LT / lambda_y) ** 2) * alpha_LT * (lambda_LT - 0.2)
            + (lambda_LT ** 2)
        )
        chi_LT = f_m / (phi_LT + math.sqrt(phi_LT ** 2 - f_m * (lambda_LT ** 2)))
        return min(chi_LT, 1.0), phi_LT

    # SECTION 17: CONNECTIONS
    @staticmethod
    def cl_17_2_1_bolt_hole_size(d, bolt_hole_type='Standard'):
        """Bolt hole diameter per Table 19 (Cl. 17.2.1)."""
        table_19 = {
            "12-14": {'Standard': 1.0, 'Over-sized': 3.0, 'short_slot': 4.0, 'long_slot': 2.5},
            "16-22": {'Standard': 2.0, 'Over-sized': 4.0, 'short_slot': 6.0, 'long_slot': 2.5},
            "24":    {'Standard': 2.0, 'Over-sized': 6.0, 'short_slot': 8.0, 'long_slot': 2.5},
            "24+":   {'Standard': 3.0, 'Over-sized': 8.0, 'short_slot': 10.0, 'long_slot': 2.5}
        }
        d_int = int(d)
        if d_int < 12:
            clearance = 0.0
        elif d_int <= 14:
            clearance = table_19["12-14"][bolt_hole_type]
        elif d_int <= 22:
            clearance = table_19["16-22"][bolt_hole_type]
        elif d_int <= 24:
            clearance = table_19["24"][bolt_hole_type]
        else:
            clearance = table_19["24+"][bolt_hole_type]
        if bolt_hole_type == 'long_slot':
            return (clearance + 1.0) * d
        return clearance + d

    @staticmethod
    def cl_17_3_3_bolt_shear_capacity(f_ub, A_nb, A_sb, n_n, n_s=0,
                                      safety_factor_parameter=KEY_DP_FAB_SHOP):
        """Design shear strength of bearing bolt (V_dsb) per Cl. 17.3.3."""
        V_nsb = (f_ub / math.sqrt(3)) * (n_n * A_nb + n_s * A_sb)
        gamma_mb = IS800_2025.cl_12_4_1_Table_5['gamma_mb'][safety_factor_parameter]
        return V_nsb / gamma_mb

    @staticmethod
    def cl_17_5_7_1_1_fillet_weld_design_stress(ultimate_stresses,
                                                fabrication=KEY_DP_FAB_SHOP):
        """Design strength of fillet weld (f_wd) per Cl. 17.5.7.1.1."""
        f_u = min(ultimate_stresses)
        f_wn = f_u / math.sqrt(3)
        gamma_mw = IS800_2025.cl_12_4_1_Table_5['gamma_mw'][fabrication]
        return f_wn / gamma_mw
