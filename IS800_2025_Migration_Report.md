# Migration of Osdag Steel Design Module: IS 800:2007 to Draft IS 800:2025

## 1. Overview
This report documents the implementation of `src/osdag/utils/common/is800_2025.py` based on the Bureau of Indian Standards **Draft IS 800:2025 (Fourth Revision, Doc: CED 07 (27869) WC, April 2025)**[cite: 8]. Following Osdag's architecture in `is800_2007.py`, the module implements key modified, newly added, and renumbered design clauses using `@staticmethod` methods inside the `IS800_2025` class[cite: 2].

## 2. Clauses & Functions Implemented
| Section | Draft IS 800:2025 Clause | Implemented Method | Status vs. IS 800:2007 |
| :--- | :--- | :--- | :--- |
| **10** | Cl. 10.8, Table 2 (i)–(vi) | `Table2_i_outstanding_element`, `Table2_ii_web_I_channel_H_box`, `Table2_iii_angle_bending`, `Table2_iv_angle_axial_compression`, `Table2_vi_circular_hollow_tube` | **Modified**[cite: 2, 46] |
| **10** | Cl. 10.9.1, Table 3 | `cl_10_9_1_max_slenderness_ratio` | **Renumbered & Bug-Fixed**[cite: 49] |
| **12** | Cl. 12.4.1, Table 5 | `cl_12_4_1_Table_5` | **Renumbered**[cite: 67] |
| **13** | Cl. 13.2, 13.3.1, 13.4.1 | `cl_13_2_tension_yielding_strength`, `cl_13_3_1_tension_rupture_strength`, `cl_13_4_1_block_shear_strength` | **Renumbered**[cite: 72, 74] |
| **14** | Cl. 14.1.2, Table 7 | `cl_14_1_2_imperfection_factor` | **Modified** (added `a0` = 0.13)[cite: 77] |
| **14** | Cl. 14.1.2.1, Tables 8 & 9 | `cl_14_1_2_1_design_compressive_stress` | **Modified**[cite: 76, 79, 84] |
| **14** | Cl. 14.1.2.2, Table 10 | `cl_14_1_2_2_buckling_class_of_cross_sections` | **Modified** ($f_y \le 420$ vs $> 420$ MPa)[cite: 89] |
| **14** | Cl. 14.4.1 | `cl_14_4_1_bearing_strength_concrete` | **Modified** (added $\sqrt{A_1/A_2}$)[cite: 91] |
| **14** | Cl. 14.5.1.2, Table 12 | `cl_14_5_1_2_single_angle_strut_one_leg` | **New Formulation** ($K_f$)[cite: 94, 95] |
| **15** | Cl. 15.2.2, Tables 13 & 14 | `cl_15_2_2_alpha_LT`, `cl_15_2_2_LTB_stress_reduction_factor` | **Modified**[cite: 106, 108, 109] |
| **17** | Cl. 17.2.1, 17.3.3, 17.5.7.1.1 | `cl_17_2_1_bolt_hole_size`, `cl_17_3_3_bolt_shear_capacity`, `cl_17_5_7_1_1_fillet_weld_design_stress` | **Renumbered**[cite: 140, 143, 152] |

## 3. Detailed Comparison: IS 800:2007 vs. Draft IS 800:2025
1. **Renumbering & Discontinuation of WSD:** Working Stress Design (Section 11 in 2007) is removed; core sections shift forward (3→10, 5→12, 6→13, 7→14, 8→15, 10→17)[cite: 10, 12].
2. **Table 2 Limits:** Outstanding compression flanges unified to $8.7\varepsilon, 9.7\varepsilon, 13.6\varepsilon$; webs tightened to $70\varepsilon, 80\varepsilon, 120\varepsilon$ (mid-depth NA) and $32\varepsilon, 36.8\varepsilon, 40.7\varepsilon$ (axial compression); circular hollow tubes updated to $47\varepsilon^2, 66\varepsilon^2, 85\varepsilon^2$ (moment) and $86\varepsilon^2$ (axial)[cite: 46].
3. **Compression Members (Section 14):** Added buckling class `a0` ($\alpha = 0.13$) and $f_y > 420$ MPa split in Table 10; concrete bearing updated to $\min(0.45 f_{ck}\sqrt{A_1/A_2}, 0.9 f_{ck})$; single angle struts loaded through one leg revised to $f_{cde} = K_f \chi_{aa} f_y / \gamma_{m0}$[cite: 77, 89, 91, 94, 95].
4. **LTB of Beams (Cl. 15.2.2):** Added Table 13 ($\alpha_{LT}$) and Table 14 ($f_m$)[cite: 108, 109].

## 4. Major Assumptions & Challenges
- **Cl. 14.1.2.1 Typo:** Draft PDF prints $\sqrt{\phi^2 + \lambda^2}$, which is a typographical error[cite: 76]. Verified against Tables 8(a)–(e) and 9(a)–(e) that $\sqrt{\phi^2 - \lambda^2}$ is required[cite: 79, 84].
- **Table 3 Legacy Bug Fix:** Fixed `is800_2007.py` returning `180` for all 6 member types[cite: 49].
- **How to Run Tests:** `python -m pytest -v tests/test_is800_2025.py`[cite: 3]

## 5. References
1. BIS, *Draft IS 800:2025 (Fourth Revision)*, Doc: CED 07 (27869) WC, April 2025[cite: 8].
2. BIS, *IS 800:2007 (Third Revision)*[cite: 1].
3. Osdag Repository: `https://github.com/osdag-admin/Osdag`[cite: 4].
4. Umesha, P. K. (2026), *IS:800-2025 - Draft Revision for General Construction in Steel: Key Developments and Required Changes*, Vol. 15, pp. 51–68[cite: 154].
