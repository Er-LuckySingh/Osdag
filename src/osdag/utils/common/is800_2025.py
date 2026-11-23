"""Module for Indian Standard, Draft IS 800 : 2025 (Fourth Revision)
Doc: CED 07 (27869) WC (April 2025)

Migrated from is800_2007.py following Osdag coding conventions.
"""
import math

try:
    from ...Common import *
except ImportError:
    # Fallback constants for standalone execution and pytest runs
    KEY_Plastic = 'Plastic'
    KEY_Compact = 'Compact'
    KEY_SemiCompact = 'Semi-Compact'
    KEY_DP_FAB_SHOP = 'Shop'
    KEY_DP_FAB_FIELD = 'Field'


class IS800_2025(object):
    """Perform structural steel design calculations as per Draft IS 800:2025."""

    # ==========================================================================
    #    SECTION 9: MATERIALS
    # ==========================================================================
    # Cl. 9.2.4.1 Physical properties of structural steel
    STEEL_DENSITY = 7850.0         # kg/m^3
    MODULUS_OF_ELASTICITY = 2.0e5  # MPa (N/mm^2)
    POISSON_RATIO = 0.3
    MODULUS_OF_RIGIDITY = 0.769e5  # MPa (N/mm^2)
    THERMAL_EXPANSION = 12e-6      # /deg C

    # ==========================================================================
    #    SECTION 10: GENERAL DESIGN REQUIREMENTS
    # ==========================================================================

    # Cl. 10.8 / Table 2: Limiting Width to Thickness Ratio
    @staticmethod
    def Table2_i_outstanding_element(width, thickness, f_y):
        """Classify an outstanding compression element under uniform compression
        as per Table 2, Sl. No. (i) of Draft IS 800:2025.

        Note: Unlike IS 800:2007, Draft IS 800:2025 unifies rolled and welded
        outstand limits to 8.7*eps (Plastic), 9.7*eps (Compact), and
        13.6*eps (Semi-compact).

        Args:
            width: Outstand width of the element in mm (float or int)
            thickness: Thickness of the element in mm (float or int)
            f_y: Yield stress of the section material in MPa (float or int)

        Returns:
            list: [section_class (str), ratio (float)]

        Reference:
            Draft IS 800:2025, Cl. 10.8 and Table 2, Sl. No. (i)
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

        Args:
            depth: Clear depth of the web in mm (float or int)
            thickness: Thickness of the web in mm (float or int)
            f_y: Yield stress of the section material in MPa (float or int)
            classification_type: 'Neutral axis at mid-depth' or 'Axial compression' (str)

        Returns:
            list: [section_class (str), ratio (float)]

        Reference:
            Draft IS 800:2025, Cl. 10.8 and Table 2, Sl. No. (ii)
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

        Args:
            width: Width of leg b in mm (float or int)
            depth: Depth of leg d in mm (float or int)
            thickness: Thickness of leg t in mm (float or int)
            f_y: Yield stress in MPa (float or int)

        Returns:
            list: [section_class (str), b_t (float), d_t (float)]

        Reference:
            Draft IS 800:2025, Cl. 10.8 and Table 2, Sl. No. (iii)
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

        Args:
            width: Width of leg b in mm (float or int)
            depth: Depth of leg d in mm (float or int)
            thickness: Thickness of leg t in mm (float or int)
            f_y: Yield stress in MPa (float or int)

        Returns:
            list: [section_class (str), b_t (float), d_t (float), bd_t (float)]

        Reference:
            Draft IS 800:2025, Cl. 10.8 and Table 2, Sl. No. (iv)
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

        Args:
            outer_diameter: Outer diameter D in mm (float or int)
            tube_thickness: Wall thickness t in mm (float or int)
            f_y: Yield stress in MPa (float or int)
            load_type: 'Axial Compression' or 'Moment' (str)

        Returns:
            list: [section_class (str), ratio (float)]

        Reference:
            Draft IS 800:2025, Cl. 10.8 and Table 2, Sl. No. (vi)
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

    # Cl. 10.9.1 / Table 3: Maximum Effective Slenderness Ratio
    @staticmethod
    def cl_10_9_1_max_slenderness_ratio(member_type=1):
        """Return the maximum effective slenderness ratio (KL/r) as per
        Table 3 (Cl. 10.9.1) of Draft IS 800:2025.

        Note: Fixes the bug in is800_2007.py where all cases returned 180.

        Args:
            member_type (int): Member category (1 to 6) per Table 3:
                1: Compression member (DL + IL) -> 180
                2: Tension member with stress reversal (non-wind/seismic) -> 180
                3: Compression from wind/earthquake combination -> 250
                4: Compression flange of beam against LTB -> 300
                5: Roof truss tie / bracing with wind/seismic reversal -> 350
                6: Members always under tension -> 400

        Returns:
            int: Maximum permissible KL/r

        Reference:
            Draft IS 800:2025, Cl. 10.9.1, Table 3
        """
        limits = {1: 180, 2: 180, 3: 250, 4: 300, 5: 350, 6: 400}
        if member_type not in limits:
            raise ValueError("member_type must be an integer between 1 and 6.")
        return limits[member_type]

    # ==========================================================================
    #    SECTION 12: LIMIT STATE DESIGN
    # ==========================================================================

    # Cl. 12.4.1 / Table 5: Partial Safety Factors for Materials, gamma_m
    cl_12_4_1_Table_5 = {
        "gamma_m0": {'yielding': 1.10, 'buckling': 1.10},
        "gamma_m1": {'ultimate_stress': 1.25},
        "gamma_mf": {KEY_DP_FAB_SHOP: 1.25, KEY_DP_FAB_FIELD: 1.25},
        "gamma_mb": {KEY_DP_FAB_SHOP: 1.25, KEY_DP_FAB_FIELD: 1.25},
        "gamma_mr": {KEY_DP_FAB_SHOP: 1.25, KEY_DP_FAB_FIELD: 1.25},
        "gamma_mw": {KEY_DP_FAB_SHOP: 1.25, KEY_DP_FAB_FIELD: 1.50}
    }

    # ==========================================================================
    #    SECTION 13: DESIGN OF TENSION MEMBERS
    # ==========================================================================

    @staticmethod
    def cl_13_2_tension_yielding_strength(A_g, f_y):
        """Calculate design strength due to yielding of gross section (T_dg).

        Args:
            A_g: Gross cross-sectional area in mm^2 (float)
            f_y: Yield stress of material in MPa (float)

        Returns:
            float: Design tension yielding strength T_dg in N

        Reference:
            Draft IS 800:2025, Cl. 13.2
        """
        gamma_m0 = IS800_2025.cl_12_4_1_Table_5["gamma_m0"]['yielding']
        return A_g * f_y / gamma_m0

    @staticmethod
    def cl_13_3_1_tension_rupture_strength(A_n, f_u):
        """Calculate design strength due to rupture of net section (T_dn).

        Args:
            A_n: Net effective area in mm^2 (float)
            f_u: Ultimate tensile stress in MPa (float)

        Returns:
            float: Design tension rupture strength T_dn in N

        Reference:
            Draft IS 800:2025, Cl. 13.3.1
        """
        gamma_m1 = IS800_2025.cl_12_4_1_Table_5["gamma_m1"]['ultimate_stress']
        return 0.9 * A_n * f_u / gamma_m1

    @staticmethod
    def cl_13_4_1_block_shear_strength(A_vg, A_vn, A_tg, A_tn, f_u, f_y):
        """Calculate block shear strength of bolted connections (T_db).

        Args:
            A_vg: Minimum gross area in shear parallel to force in mm^2 (float)
            A_vn: Minimum net area in shear parallel to force in mm^2 (float)
            A_tg: Minimum gross area in tension perpendicular to force in mm^2 (float)
            A_tn: Minimum net area in tension perpendicular to force in mm^2 (float)
            f_u: Ultimate stress of material in MPa (float)
            f_y: Yield stress of material in MPa (float)

        Returns:
            float: Block shear strength T_db in N

        Reference:
            Draft IS 800:2025, Cl. 13.4.1
        """
        gamma_m0 = IS800_2025.cl_12_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2025.cl_12_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_db1 = (A_vg * f_y / (math.sqrt(3) * gamma_m0)) + (0.9 * A_tn * f_u / gamma_m1)
        T_db2 = (0.9 * A_vn * f_u / (math.sqrt(3) * gamma_m1)) + (A_tg * f_y / gamma_m0)
        return min(T_db1, T_db2)

    # ==========================================================================
    #    SECTION 14: DESIGN OF COMPRESSION MEMBERS
    # ==========================================================================

    # Cl. 14.1.1 & 14.1.2 / Table 7: Imperfection Factor, alpha
    @staticmethod
    def cl_14_1_2_imperfection_factor(buckling_class):
        """Return imperfection factor alpha for column buckling class
        (includes new class 'a0' = 0.13 in Draft IS 800:2025).

        Args:
            buckling_class (str): 'a0', 'a', 'b', 'c', or 'd'

        Returns:
            float: Imperfection factor alpha

        Reference:
            Draft IS 800:2025, Cl. 14.1.1, Cl. 14.1.2, Table 7
        """
        table_7 = {'a0': 0.13, 'a': 0.21, 'b': 0.34, 'c': 0.49, 'd': 0.76}
        if buckling_class not in table_7:
            raise ValueError(f"Invalid buckling_class '{buckling_class}'. Must be one of {list(table_7.keys())}.")
        return table_7[buckling_class]

    # Cl. 14.1.2.1: Reduction Factor & Design Compressive Stress (Flexural Buckling)
    @staticmethod
    def cl_14_1_2_1_design_compressive_stress(f_y, effective_slenderness_ratio,
                                              buckling_class,
                                              modulus_of_elasticity=2.0e5):
        """Calculate flexural buckling stress reduction factor (chi) and design
        compressive stress (f_cd) per Cl. 14.1.2.1 of Draft IS 800:2025.

        Assumption:
            The printed draft equation in Cl. 14.1.2.1 shows a '+' sign inside
            sqrt(phi^2 + lambda^2), which is a typographical error. The standard
            Perry-Robertson formula sqrt(phi^2 - lambda^2) is used here because
            it exactly reproduces all tabulated values in Table 8(a)-(e) and
            Table 9(a)-(e) of Draft IS 800:2025.

        Args:
            f_y: Yield stress in MPa (float)
            effective_slenderness_ratio: KL/r (float)
            buckling_class: 'a0', 'a', 'b', 'c', or 'd' (str)
            modulus_of_elasticity: Young's modulus E in MPa (default 2e5)

        Returns:
            dict: {'f_cr', 'lambda', 'phi', 'chi', 'f_cd'}

        Reference:
            Draft IS 800:2025, Cl. 14.1.2, Cl. 14.1.2.1, Tables 7, 8, 9
        """
        gamma_m0 = IS800_2025.cl_12_4_1_Table_5["gamma_m0"]['buckling']
        alpha = IS800_2025.cl_14_1_2_imperfection_factor(buckling_class)

        f_cr = (math.pi ** 2 * modulus_of_elasticity) / (effective_slenderness_ratio ** 2)
        lam = math.sqrt(f_y / f_cr)
        phi = 0.5 * (1.0 + alpha * (lam - 0.2) + lam ** 2)
        chi = min(1.0 / (phi + math.sqrt(phi ** 2 - lam ** 2)), 1.0)
        f_cd = min(chi * f_y / gamma_m0, f_y / gamma_m0)

        return {
            'f_cr': f_cr,
            'lambda': lam,
            'phi': phi,
            'chi': chi,
            'f_cd': f_cd
        }

    # Cl. 14.1.2.2 / Table 10: Buckling Class of Cross Sections
    @staticmethod
    def cl_14_1_2_2_buckling_class_of_cross_sections(b_f, h, t_f, f_y=250.0,
                                                     cross_section='Rolled I-sections',
                                                     section_type='Hot rolled'):
        """Determine buckling class about z-z and y-y axes as per Table 10
        of Draft IS 800:2025 (updated to distinguish f_y <= 420 MPa and f_y > 420 MPa).

        Args:
            b_f: Flange width in mm (float)
            h: Overall depth of section in mm (float)
            t_f: Flange thickness in mm (float)
            f_y: Yield stress in MPa (float, default 250.0)
            cross_section: 'Rolled I-sections', 'Welded I-section', 'Hollow Section',
                           'Channel, Angle, T, Solid', 'Built-up Member' (str)
            section_type: 'Hot rolled' or 'Cold formed' (for Hollow Section) (str)

        Returns:
            dict: {'z-z': str, 'y-y': str}

        Reference:
            Draft IS 800:2025, Cl. 14.1.2.2, Table 10
        """
        high_strength = f_y > 420.0

        if cross_section == 'Rolled I-sections':
            if h / b_f > 1.2:
                if t_f <= 40:
                    return {'z-z': 'a0', 'y-y': 'a'} if high_strength else {'z-z': 'a', 'y-y': 'b'}
                elif t_f <= 100:
                    return {'z-z': 'a', 'y-y': 'b'} if high_strength else {'z-z': 'b', 'y-y': 'c'}
                else:
                    return {'z-z': 'd', 'y-y': 'd'}
            else:
                if t_f <= 100:
                    return {'z-z': 'a', 'y-y': 'a'} if high_strength else {'z-z': 'b', 'y-y': 'c'}
                else:
                    return {'z-z': 'c', 'y-y': 'c'} if high_strength else {'z-z': 'd', 'y-y': 'd'}

        elif cross_section == 'Welded I-section':
            if t_f <= 40:
                return {'z-z': 'b', 'y-y': 'c'}
            else:
                return {'z-z': 'c', 'y-y': 'd'}

        elif cross_section == 'Hollow Section':
            if section_type == 'Hot rolled':
                cls = 'a0' if high_strength else 'a'
                return {'z-z': cls, 'y-y': cls}
            else:
                cls = 'c' if high_strength else 'b'
                return {'z-z': cls, 'y-y': cls}

        elif cross_section in ('Channel, Angle, T, Solid', 'Built-up Member'):
            return {'z-z': 'c', 'y-y': 'c'}

        else:
            raise ValueError(f"Unsupported cross_section: {cross_section}")

    # Cl. 14.4.1: Column Bases - Bearing Strength of Concrete
    @staticmethod
    def cl_14_4_1_bearing_strength_concrete(concrete_grade, A_1=1.0, A_2=1.0):
        """Calculate maximum permissible bearing strength of concrete pedestal
        as per Cl. 14.4.1 of Draft IS 800:2025.

        Updated from IS 800:2007 (0.45 * f_ck) to:
            min(0.45 * f_ck * sqrt(A_1 / A_2), 0.9 * f_ck)

        Args:
            concrete_grade: Concrete grade string, e.g. 'M20', 'M25', 'M30' (str)
            A_1: Area of concrete pedestal on which base plate sits in mm^2 (float)
            A_2: Surface area of steel base plate transferring load in mm^2 (float)

        Returns:
            float: Maximum bearing strength in MPa (N/mm^2)

        Reference:
            Draft IS 800:2025, Cl. 14.4.1
        """
        f_ck_map = {
            'M10': 10, 'M15': 15, 'M20': 20, 'M25': 25, 'M30': 30,
            'M35': 35, 'M40': 40, 'M45': 45, 'M50': 50, 'M55': 55, 'M60': 60
        }
        f_ck = f_ck_map[str(concrete_grade)]
        return min(0.45 * f_ck * math.sqrt(A_1 / A_2), 0.9 * f_ck)

    # Cl. 14.5.1.2 / Table 12: Single Angle Strut Loaded Through One Leg
    @staticmethod
    def cl_14_5_1_2_single_angle_strut_one_leg(l_aa, r_aa, b1, b2, t, f_y,
                                               bolt_no=2, fixity='Fixed',
                                               modulus_of_elasticity=2.0e5):
        """Calculate design compressive stress (f_cde) for a single angle strut
        loaded through one leg as per Cl. 14.5.1.2 and Table 12 of Draft IS 800:2025.

        Completely revised from IS 800:2007 (which used an equivalent slenderness
        ratio). Draft IS 800:2025 uses:
            f_cde = K_f * chi_aa * f_y / gamma_m0
            K_f = k1 + k2 * lambda_aa + k3 * lambda_phi

        Args:
            l_aa: Unsupported length perpendicular to a-a axis in mm (float)
            r_aa: Radius of gyration about a-a axis in mm (float)
            b1: Width of connected leg in mm (float)
            b2: Width of outstanding leg in mm (float)
            t: Thickness of angle leg in mm (float)
            f_y: Yield stress in MPa (float)
            bolt_no: Number of bolts (>= 2 or 1; welded treated as >= 2) (int)
            fixity: 'Fixed', 'Hinged', or 'Partial' (str)
            modulus_of_elasticity: Young's modulus E in MPa (default 2e5)

        Returns:
            dict: {'f_cde', 'K_f', 'chi_aa', 'lambda_aa', 'lambda_phi'}

        Reference:
            Draft IS 800:2025, Cl. 14.5.1.2, Table 12
        """
        gamma_m0 = IS800_2025.cl_12_4_1_Table_5["gamma_m0"]['buckling']
        epsilon = math.sqrt(250.0 / f_y)
        denom = epsilon * math.sqrt((math.pi ** 2 * modulus_of_elasticity) / 250.0)

        lambda_aa = (l_aa / r_aa) / denom
        lambda_phi = ((b1 + b2) / (2.0 * t)) / denom

        # Stress reduction factor chi_aa for buckling class 'b' (alpha = 0.34)
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
            K_f_fixed = k1_f + k2_f * lambda_aa + k3_f * lambda_phi
            K_f_hinged = k1_h + k2_h * lambda_aa + k3_h * lambda_phi
            K_f = 0.5 * (K_f_fixed + K_f_hinged)
        else:
            raise ValueError(f"Invalid fixity: {fixity}")

        f_cde = K_f * chi_aa * f_y / gamma_m0
        return {
            'f_cde': f_cde,
            'K_f': K_f,
            'chi_aa': chi_aa,
            'lambda_aa': lambda_aa,
            'lambda_phi': lambda_phi
        }

    # ==========================================================================
    #    SECTION 15: DESIGN OF MEMBERS SUBJECTED TO BENDING
    # ==========================================================================

    # Cl. 15.2.2 / Table 13: Imperfection Parameter alpha_LT for LTB
    @staticmethod
    def cl_15_2_2_alpha_LT(cross_section, h, b_min, t_f=None, Z_ez=None, Z_ey=None):
        """Calculate the lateral torsional buckling imperfection parameter
        alpha_LT as per Table 13 (Cl. 15.2.2) of Draft IS 800:2025.

        Args:
            cross_section (str): 'Rolled I/H', 'Welded I', 'Rolled unequal I/H',
                                 'Welded unequal I', or 'Other rolled'
            h (float): Depth of section in mm
            b_min (float): Minimum flange width in mm
            t_f (float, optional): Flange thickness in mm
            Z_ez (float, optional): Elastic modulus about major axis z-z
            Z_ey (float, optional): Elastic modulus about minor axis y-y

        Returns:
            float: Imperfection parameter alpha_LT

        Reference:
            Draft IS 800:2025, Cl. 15.2.2, Table 13
        """
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
        else:
            raise ValueError(f"Unsupported cross_section: {cross_section}")

    # Cl. 15.2.2: Laterally Unsupported Beam Reduction Factor chi_LT
    @staticmethod
    def cl_15_2_2_LTB_stress_reduction_factor(lambda_LT, lambda_y, alpha_LT, f_m=1.0):
        """Calculate bending stress reduction factor chi_LT for laterally
        unsupported beams as per Cl. 15.2.2 of Draft IS 800:2025.

        Args:
            lambda_LT: Non-dimensional LTB slenderness ratio (float)
            lambda_y: Non-dimensional weak-axis slenderness ratio (float)
            alpha_LT: Imperfection parameter from Table 13 (float)
            f_m: Moment gradient effect parameter from Table 14 (default 1.0)

        Returns:
            tuple: (chi_LT (float), phi_LT (float))

        Reference:
            Draft IS 800:2025, Cl. 15.2.2, Tables 13 & 14
        """
        if lambda_LT < 0.4:
            return 1.0, 0.5

        phi_LT = 0.5 * (
            1.0 + f_m * ((lambda_LT / lambda_y) ** 2) * alpha_LT * (lambda_LT - 0.2)
            + (lambda_LT ** 2)
        )
        chi_LT = f_m / (phi_LT + math.sqrt(phi_LT ** 2 - f_m * (lambda_LT ** 2)))
        return min(chi_LT, 1.0), phi_LT

    # ==========================================================================
    #    SECTION 17: CONNECTIONS
    # ==========================================================================

    @staticmethod
    def cl_17_2_1_bolt_hole_size(d, bolt_hole_type='Standard'):
        """Calculate bolt hole diameter as per Table 19 (Cl. 17.2.1) of Draft IS 800:2025."""
        table_19 = {
            "12-14": {'Standard': 1.0, 'Over-sized': 3.0, 'short_slot': 4.0, 'long_slot': 2.5},
            "16-22": {'Standard': 2.0, 'Over-sized': 4.0, 'short_slot': 6.0, 'long_slot': 2.5},
            "24":    {'Standard': 2.0, 'Over-sized': 6.0, 'short_slot': 8.0, 'long_slot': 2.5},
            "24+":   {'Standard': 3.0, 'Over-sized': 8.0, 'short_slot': 10.0, 'long_slot': 2.5}
        }
        d_int = int(d)
        if d_int < 12:
            clearance = 0.
