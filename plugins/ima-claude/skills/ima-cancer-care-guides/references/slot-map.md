# Cancer Care Guide — Template Slot Map

Template source: Cancer Drug Resistance Guide (`DAHC5t-HGsk`)
Copy for testing: `DAHDW5GY03s`

This maps every element in the template design to a named slot.
To create a new guide, duplicate the template in Canva, then use `replace_text`
with the element IDs to swap content slot by slot.

> **Confirmed**: Element IDs are preserved when a design is duplicated (File → Make a copy).
> The IDs below can be used directly on any copy of the template without re-mapping.

---

## Page 1 — Cover Page

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `cover_logo` | `PBhMCnWGZWhcwN0p-LB3r33FMvsNQRPzv` | IMAGE (fill) | IMA logo (asset: MAGc82phFhw) — NOT editable via API |
| `cover_navy_band` | `PBhMCnWGZWhcwN0p-LBkQQ4KwWrfkwqxk` | SHAPE | Navy blue band behind "CANCER" — no text |
| `cover_title_1` | `PBhMCnWGZWhcwN0p-LB5Dfy4LKBHLbvZ2` | TEXT | "cancer" (large white text in navy band) |
| `cover_title_2` | `PBhMCnWGZWhcwN0p-LBBB35r43HBY5VV8` | TEXT | "Resistance" (large dark text below band) |
| `cover_subtitle` | `PBhMCnWGZWhcwN0p-LBTJXp22Y0Hg7CWx` | TEXT | "And Interventions to Mitigate Resistance" |
| `cover_authors` | `PBhMCnWGZWhcwN0p-LBLDVg5Z9qfRZsLS` | TEXT | "Paul E. Marik, MD, FCCM, FCCP\nJustus R. Hope, MD" |
| `cover_book_image` | `PBhMCnWGZWhcwN0p-LBhQKJ9mgY3RVGmc` | IMAGE (fill) | Cancer Care book thumbnail (asset: MAGgbJNkJJA) — editable |
| `cover_disclaimer` | `PBhMCnWGZWhcwN0p-LB5BKJbRpVCbpX5N` | TEXT | "This guide outlines our complementary approach to the use of repurposed drugs in cancer treatment. It is not intended as a comprehensive reference. The full guide, \"Cancer Care: The Role of Repurposed Drugs and Metabolic Interventions in Treating Cancer,\" including all scientific references, is available at imahealth.org/research/cancer-care." |
| `cover_date` | `PBhMCnWGZWhcwN0p-LBWkKcxh68wh1BzW` | TEXT | "Updated March 2026" |

---

## Page 2 — Introduction

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `intro_heading` | `PBhzHx5FDf3N5L3x-LBrQmFjfT0B2CHtH` | TEXT | "Introduction" |
| `intro_body` | `PBhzHx5FDf3N5L3x-LBWrc7qLRWTCtN7w` | TEXT | "Caution to the reader: This is a complex and evolving topic..." (full intro with critical questions) |
| `intro_warning_box_shape` | `PBhzHx5FDf3N5L3x-LBT9zKDJCwdNzVD6-LBQ602qfPkkND83P` | SHAPE | Yellow/beige warning box background |
| `intro_warning_text` | `PBhzHx5FDf3N5L3x-LBT9zKDJCwdNzVD6-LB6VrTxBz5YNrXW8` | TEXT | "Cancer is a complicated disease, and patient care should be supervised by an integrative clinician; patients should not treat themselves." |
| `intro_footer` | `PBhzHx5FDf3N5L3x-LBXT1qDqQCt6Zr62` | TEXT | "Cancer-Resistance and Interventions to Mitigate Resistance (03/04/2026)" |

---

## Page 3 — Biological Basis of Metabolic Resistance

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p3_section_heading` | `PBWtNbsXQgDt7wjt-LBldFnrRxCXJW7cN` | TEXT | "Biological Basis of Metabolic Resistance" |
| `p3_sub1_heading` | `PBWtNbsXQgDt7wjt-LBznHXYR2G1qBSC0` | TEXT | "Evolutionary dynamics under chronic pressure" |
| `p3_sub1_body` | `PBWtNbsXQgDt7wjt-LB2fJwGXqc5yHKxJ` | TEXT | "This scenario reflects acquired therapeutic resistance..." (3 paragraphs) |
| `p3_sub2_heading` | `PBWtNbsXQgDt7wjt-LB3glG0mHmSvPl6k` | TEXT | "Metabolic plasticity as a central driver" |
| `p3_sub2_body` | `PBWtNbsXQgDt7wjt-LBwyZFxS1wb11fgC` | TEXT | "This adaptive flexibility is rooted in metabolic plasticity..." |
| `p3_footer` | `PBWtNbsXQgDt7wjt-LBJFzYxv28X3s0m6` | TEXT | Footer with title and date |

---

## Page 4 — Stress Signaling, Epigenetic Adaptation

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p4_sub_heading` | `PBtLlbGbqQlsQ2Dq-LBBLLkZdrVvWbbYB` | TEXT | "Stress signaling, epigenetic adaptation, and redox remodeling" |
| `p4_body` | `PBtLlbGbqQlsQ2Dq-LB6hNkPwxTD2m4CM` | TEXT | "Continuous exposure to polyphenols and metabolic drugs can remodel signaling..." |
| `p4_footer` | `PBtLlbGbqQlsQ2Dq-LBJTlcMHLXTZZkfP` | TEXT | Footer |

---

## Page 5 — Key Drivers of Resistance

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p5_section_heading` | `PBVkL3jZMs9w0hy6-LBrx3Z4Ys2d9Qg3D` | TEXT | "Key Drivers of Resistance Under Metabolic Pressure" |
| `p5_sub1_heading` | `PBVkL3jZMs9w0hy6-LBLcS2WXmvyNTslw` | TEXT | "Metabolic plasticity and switching" |
| `p5_sub1_body` | `PBVkL3jZMs9w0hy6-LBkLtjKT8jyJYfmm` | TEXT | "Tumors and CSCs switch between glycolysis and OXPHOS..." |
| `p5_sub2_heading` | `PBVkL3jZMs9w0hy6-LBXMxn2CDhmK4pwn` | TEXT | "Enrichment of CSC-like subpopulations" |
| `p5_sub2_body` | `PBVkL3jZMs9w0hy6-LBH8rX01xVbVQzBb` | TEXT | "CSCs exhibit marked metabolic flexibility..." |
| `p5_sub3_heading` | `PBVkL3jZMs9w0hy6-LBNJ8Qhfwfpbb56w` | TEXT | "Adaptive stress signaling and transcriptional reprogramming" |
| `p5_sub3_body` | `PBVkL3jZMs9w0hy6-LB4yvbnzdcmk4Qwx` | TEXT | "Targeted inhibition of oncogenic signaling..." |
| `p5_sub4_heading` | `PBVkL3jZMs9w0hy6-LBMNSDmdcx2frzQb` | TEXT | "Microenvironmental and niche-level adaptation" |
| `p5_sub4_body` | `PBVkL3jZMs9w0hy6-LBN862wrYqBrMnhS` | TEXT | "Stromal cells, immune infiltrates..." |
| `p5_footer` | `PBVkL3jZMs9w0hy6-LBw5Qb7zRnSr9yw2` | TEXT | Footer |

---

## Page 6 — Genetic Hardening + Why Double-Edged

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p6_sub1_heading` | `PBxbMpBp1SF3Gw01-LB35TcrkfRdc41dH` | TEXT | "Genetic and epigenetic hardening over time" |
| `p6_sub1_body` | `PBxbMpBp1SF3Gw01-LBvlv2CGwY5D2T9j` | TEXT | "Repeated or chronic sublethal stress selects..." |
| `p6_section_heading` | `PBxbMpBp1SF3Gw01-LBx6szB0KQ3Fh9J3` | TEXT | "Why Multi-Agent Metabolic Regimens Are Double-Edged" |
| `p6_section_body` | `PBxbMpBp1SF3Gw01-LBDcWzzsCgNKVtgt` | TEXT | "Multi-agent metabolic combinations aim to exert synergistic pressure..." |
| `p6_bullets` | `PBxbMpBp1SF3Gw01-LBjMBVMtVX5Sr4gG` | TEXT | "If dosing intensity is kept in a tolerable band..." (2 bullet points) |
| `p6_footer` | `PBxbMpBp1SF3Gw01-LBN0XzT1tkR0Ffc8` | TEXT | Footer |

---

## Page 7 — Chronic Flat Regimens + Press-Pulse

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p7_section1_heading` | `PBWCm4dkxKM0hpdM-LBkBGfcDJDbXm4KY` | TEXT | "Why Chronic, Flat Multi-Agent Regimens Are Risky" |
| `p7_section1_body` | `PBWCm4dkxKM0hpdM-LB7vQ8YzSQDMpShG` | TEXT | "Flat, continuous dosing of multiple repurposed drugs..." |
| `p7_section2_heading` | `PBWCm4dkxKM0hpdM-LBDDNtlDf0PBVjng` | TEXT | "Role of Press–Pulse and Adaptive Therapy" |
| `p7_section2_body` | `PBWCm4dkxKM0hpdM-LBztmZs0Z7xN61dd` | TEXT | "Press–pulse strategies apply a chronic press..." |
| `p7_footer` | `PBWCm4dkxKM0hpdM-LBDQ93mMPf0q14Bw` | TEXT | Footer |

---

## Page 8 — Practical Design Strategies

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p8_section_heading` | `PBz8Fhlwy5YKvYTp-LBbDPsm5NL7rZHQV` | TEXT | "Practical Design Strategies" |
| `p8_intro` | `PBz8Fhlwy5YKvYTp-LBBJnMx2H1FJKqCJ` | TEXT | "When building multi-agent protocols..." |
| `p8_sub1_heading` | `PBz8Fhlwy5YKvYTp-LBdnv5NFgrbzCsW1` | TEXT | "Timestructured press–pulse scheduling(16)" |
| `p8_sub1_body` | `PBz8Fhlwy5YKvYTp-LBZJ5q6gsRHPfpQm` | TEXT | "Use chronic press elements..." |
| `p8_sub2_heading` | `PBz8Fhlwy5YKvYTp-LBk9gxB6nQhZQ4l0` | TEXT | "Rotating and modular combinations(15)" |
| `p8_sub2_body` | `PBz8Fhlwy5YKvYTp-LB0dGMKsRB5W5VVl` | TEXT | "Rotate subsets of agents..." |
| `p8_sub3_heading` | `PBz8Fhlwy5YKvYTp-LB25p3bNGddHFBJR` | TEXT | "Explicit CSC and plasticity targeting(17)" |
| `p8_sub3_body` | `PBz8Fhlwy5YKvYTp-LBtXc9ns1BXGTyjD` | TEXT | "Include agents and pulses known to debulk..." |
| `p8_sub4_heading` | `PBz8Fhlwy5YKvYTp-LBy8wrGxqYC6kRBf` | TEXT | "Dosing intensity and sequence optimization(17)" |
| `p8_sub4_body` | `PBz8Fhlwy5YKvYTp-LByW9t7lrJjwfJNl` | TEXT | "Aim for clearly cytotoxic or cytostatic pulses..." |
| `p8_footer` | `PBz8Fhlwy5YKvYTp-LBd0tLxN8YXgqD3y` | TEXT | Footer |

---

## Page 9 — Multi-Agent Protocol

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p9_section_heading` | `PB1ffcW4zXK4fMXX-LBhWX5f3N45TMsG2` | TEXT | "Multi-Agent Protocol: Adaptive Resistance Considerations" |
| `p9_intro` | `PB1ffcW4zXK4fMXX-LBd8DHnBfj494L2g` | TEXT | "The proposed multi-agent protocol combines vitamin D, curcumin..." |
| `p9_sub_heading` | `PB1ffcW4zXK4fMXX-LB0kRLCTtxQ36Hmr` | TEXT | "What the protocol is doing" |
| `p9_sub_intro` | `PB1ffcW4zXK4fMXX-LBt8BSBy6h0CzckH` | TEXT | "Core elements and dominant pressures:" |
| `p9_core_elements` | `PB1ffcW4zXK4fMXX-LBjn66lhKZbcnmmS` | TEXT | "Metabolic/AMPK–mTOR axis: ... CSC-targeting phytochemicals... Anti-CSC repurposed drugs... Microenvironment/stress modulation... Net effect..." |
| `p9_footer` | `PB1ffcW4zXK4fMXX-LBssmpn6K121Fkv3` | TEXT | Footer |

---

## Page 10 — Likely Escape Routes

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p10_sub_heading` | `PBhGFsQrxrhmCn4c-LBNprWXHdPnZwMsv` | TEXT | "Likely escape routes under chronic use" |
| `p10_intro` | `PBhGFsQrxrhmCn4c-LBMMVD3BKPKHc57S` | TEXT | "Even with strong CSC coverage, a static protocol will tend to select for:" |
| `p10_body` | `PBhGFsQrxrhmCn4c-LBdn0JBT6LY762pc` | TEXT | "Shift to OXPHOS/FAO... Emergence of slowcycling... Microenvironmental buffering... Pharmacokinetic gaps..." |
| `p10_footer` | `PBhGFsQrxrhmCn4c-LB7g0dBk6dR3T5Q1` | TEXT | Footer |

---

## Page 11 — Practical Modifications

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p11_section_heading` | `PBpPJq2Lkjpbyp79-LBfDh3SNTQjhP7S8` | TEXT | "Practical Modifications to Reduce Adaptive Resistance" |
| `p11_sub1_heading` | `PBpPJq2Lkjpbyp79-LBl7YwLDTMvLPfCB` | TEXT | "Introduce pulsing and drug rotation" |
| `p11_sub1_body` | `PBpPJq2Lkjpbyp79-LBhGtNWS9pf8v80s` | TEXT | "Goal: avoid chronic, tolerable stress..." |
| `p11_sub2_heading` | `PBpPJq2Lkjpbyp79-LByjR9JSPy3Bbn3l` | TEXT | "Core Care Oncology metabolic protocol drugs" |
| `p11_sub2_body` | `PBpPJq2Lkjpbyp79-LBf8mPy6sMXl1S1X` | TEXT | "The standard protocol uses metformin, atorvastatin..." |
| `p11_sub3_heading` | `PBpPJq2Lkjpbyp79-LBrmLBGjKhh3ZJwJ` | TEXT | "How mebendazole and doxycycline are cycled" |
| `p11_sub3_body` | `PBpPJq2Lkjpbyp79-LBrD9FNSjZKc1JHs` | TEXT | "Patient-facing descriptions indicate..." |
| `p11_sub4_heading` | `PBpPJq2Lkjpbyp79-LBrHlY9hsyg8FG90` | TEXT | "Why cycling matters for resistance" |
| `p11_sub4_body` | `PBpPJq2Lkjpbyp79-LBdZ819rHgpcRQt6` | TEXT | "Alternating mebendazole and doxycycline applies sequential pressure..." |
| `p11_footer` | `PBpPJq2Lkjpbyp79-LBQ7GM6Xc92WGt9b` | TEXT | Footer |

---

## Page 12 — Anchor Combinations + Rebalance + Propranolol/Melatonin

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p12_sub1_heading` | `PBMZd3hdvX42k2sg-LBnT8DddynYMJqwb` | TEXT | "Anchor combinations with cytotoxic or local therapies when possible" |
| `p12_sub1_body` | `PBMZd3hdvX42k2sg-LB15519hzXrwfzCQ` | TEXT | "This protocol is inherently adjunctive..." |
| `p12_sub2_heading` | `PBMZd3hdvX42k2sg-LBw1ZH0NRzc0YlcS` | TEXT | "Rebalance CSC versus non-CSC pressure" |
| `p12_sub2_intro` | `PBMZd3hdvX42k2sg-LBmZQl984lbZSyFs` | TEXT | "This protocol is heavily CSC-oriented..." |
| `p12_sub2_body` | `PBMZd3hdvX42k2sg-LBFb2qlx3FsJzTJS` | TEXT | "Combine core CSC phytochemicals... Synchronize ivermectin..." |
| `p12_sub3_heading` | `PBMZd3hdvX42k2sg-LBhjS13hCFrZ93fM` | TEXT | "Use propranolol and melatonin strategically" |
| `p12_sub3_intro` | `PBMZd3hdvX42k2sg-LBtCFMCy7gb7BQGz` | TEXT | "Rather than background use only:" |
| `p12_sub3_body` | `PBMZd3hdvX42k2sg-LB13HgQn6nQjRttS` | TEXT | "Propranolol may be most valuable around surgery..." |
| `p12_footer` | `PBMZd3hdvX42k2sg-LBwmpwnr3GHG30wq` | TEXT | Footer |

---

## Page 13 — Example Adaptive Schedules

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p13_section_heading` | `PBwpzZlLy5pRPvNK-LBhHRY4khg5hQKm6` | TEXT | "Example Adaptive Schedules" |
| `p13_sub1_heading` | `PBwpzZlLy5pRPvNK-LBmSmvfcBmr2HrYN` | TEXT | "Adjunctive anti-resistance schedule (with chemo/RT) (See Figure 2)" |
| `p13_sub1_body` | `PBwpzZlLy5pRPvNK-LBxBc1jq1ZN43yPz` | TEXT | "One possible pattern: Weeks 1–4: ... Weeks 5–8: ... Cytotoxic/RT windows: ..." |
| `p13_sub2_heading` | `PBwpzZlLy5pRPvNK-LBpPx6rH1BWgBwsn` | TEXT | "Stand-alone anti-resistance schedule (no chemo/RT)" |
| `p13_sub2_body` | `PBwpzZlLy5pRPvNK-LBh1BXRCPyWVk6Kf` | TEXT | "For standalone use, the same principles apply..." |
| `p13_sub2_label` | `PBwpzZlLy5pRPvNK-LBJS6kg2dGQ9YThg` | TEXT | "Core structure" |
| `p13_sub2_details` | `PBwpzZlLy5pRPvNK-LBhzXrTN6zYTZTW0` | TEXT | "Attack windows: ... Maintenance windows: ..." |
| `p13_coc_heading` | `PBwpzZlLy5pRPvNK-LBCDNh9Zv763sJJ8` | TEXT | "COC-style one-month doxycycline/one-month mebendazole cycling..." |
| `p13_coc_label` | `PBwpzZlLy5pRPvNK-LB5RnVgBZMM9l3DJ` | TEXT | "Overall, eight-week cycle" |
| `p13_coc_block_a` | `PBwpzZlLy5pRPvNK-LBbtZHStXh3kFt4z` | TEXT | "Weeks 1–4 (Attack Block A – doxycycline month)..." |
| `p13_footer` | `PBwpzZlLy5pRPvNK-LBL2ttggsPbWvPwy` | TEXT | Footer |

---

## Page 14 — COC Cycle Continued

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p14_block_a_cont` | `PBssVqvC2ZSP4Qcp-LBQ0T0S69j9rqzkF` | TEXT | "Microenvironment/support: Propranolol... Goal: Strong AMPK–mTOR inhibition..." |
| `p14_block_b_label` | `PBssVqvC2ZSP4Qcp-LBMh0rwT5qZQhhs0` | TEXT | "Weeks 5–8 (Attack Block B—mebendazole month)" |
| `p14_block_b_body` | `PBssVqvC2ZSP4Qcp-LBh3jMFPCCBxcX7n` | TEXT | "Metabolic backbone: Metformin + berberine... CSC/cytoskeleton: Mebendazole... Goal: maintain metabolic stress..." |
| `p14_footer` | `PBssVqvC2ZSP4Qcp-LBRGHXDdJ4PPFq5P` | TEXT | Footer |

---

## Page 15 — Figures 1 & 2

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p15_fig1_caption` | `PBG1T8SmdnbBZfly-LBzryqSJt5TJfLrH` | TEXT | "Figure 1. Approach to prevent adaptive resistance in multi-agent metabolic protocols." |
| `p15_fig1_image` | `PBG1T8SmdnbBZfly-LB6gbPcZLWhr6QWH` | IMAGE (fill) | Figure 1 diagram (asset: MAHDKJrLvnU) — editable |
| `p15_fig2_caption` | `PBG1T8SmdnbBZfly-LBsfq40N1LmGcx1Z` | TEXT | "Figure 2. Adjunctive adaptive metabolic therapy rotation strategy with chemotherapy or radiotherapy." |
| `p15_fig2_image` | `PBG1T8SmdnbBZfly-LBJzHLpSDzhdgY9g` | IMAGE (fill) | Figure 2 diagram (asset: MAHDAR3S6Ss) — editable |
| `p15_footer` | `PBG1T8SmdnbBZfly-LBglVRqsyf2hFP5V` | TEXT | Footer |

---

## Page 16 — Figures 3 & 4

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p16_fig3_caption` | `PBGrBKX0cgFypmlV-LByqb7znzXqfKCK4` | TEXT | "Figure 3. Standalone adaptive metabolic therapy dosing strategy..." |
| `p16_fig3_image` | `PBGrBKX0cgFypmlV-LBCZFbxjMv53DXc1` | IMAGE (fill) | Figure 3 diagram (asset: MAHDBcqymFY) — editable |
| `p16_mcp_note` | `PBGrBKX0cgFypmlV-LBwSB6l62P0lm1qV` | TEXT | "Modified Citrus Pectin (if appropriate) should be taken daily." |
| `p16_mcp_arrow` | `PBGrBKX0cgFypmlV-LBnsPV8KtP46pHGW` | IMAGE (fill) | Small arrow graphic (asset: MAG7EqZeGgI) |
| `p16_fig4_caption` | `PBGrBKX0cgFypmlV-LBDZDK06VnJKxYxf` | TEXT | "Figure 4. Simplified schematic of an eight-week stand-alone cyclical metabolic targeting protocol." |
| `p16_fig4_image` | `PBGrBKX0cgFypmlV-LBsLljmrMbWJKj2c` | IMAGE (fill) | Figure 4 diagram (asset: MAHDE_iyxKk) — editable |
| `p16_footer` | `PBGrBKX0cgFypmlV-LBB3lmtYcDRJ44Fp` | TEXT | Footer |

---

## Page 17 — Explanatory Notes (Q1 & Q2)

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p17_section_heading` | `PBT3NfSBl92cKF8W-LBW5TP0PNMT9MGbV` | TEXT | "Explanatory Notes" |
| `p17_q1_heading` | `PBT3NfSBl92cKF8W-LBx4CCGpncg5pwYD` | TEXT | "Should metformin and berberine be cycled separately in alternating months?" |
| `p17_q1_body` | `PBT3NfSBl92cKF8W-LBzmtDgssxy88qNy` | TEXT | "NO. Cycling them is likely inferior to combining them..." (full detailed answer) |
| `p17_q2_heading` | `PBT3NfSBl92cKF8W-LB3yg7SNcNy6W05m` | TEXT | "Should metformin + berberine be cycled in alternating months?" |
| `p17_q2_body` | `PBT3NfSBl92cKF8W-LBNjBzT8mzVFPV23` | TEXT | "NO. Separating them would remove the documented combination effect..." |
| `p17_footer` | `PBT3NfSBl92cKF8W-LBXK4lYvxpWzRXxq` | TEXT | Footer |

---

## Page 18 — Explanatory Notes (Q2 cont, Q3, Q4)

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p18_q2_cont` | `PBzrpvyyg1wXRRWr-LBgHpM1lzH5KNYjz` | TEXT | "Standalone (no chemotherapy): Alternating use is likely acceptable..." |
| `p18_q3_heading` | `PBzrpvyyg1wXRRWr-LBzCrBZpRV9PGB89` | TEXT | "Should ivermectin be cycled in alternating months?" |
| `p18_q3_body` | `PBzrpvyyg1wXRRWr-LBsbns5Jt85w7BmN` | TEXT | "NO. In the original protocol, the maintenance window relies on phytochemicals..." (long answer) |
| `p18_q4_heading` | `PBzrpvyyg1wXRRWr-LBXtZwPLr6lk2yM0` | TEXT | "Should omega-3 fatty acids be added to reduce resistance?" |
| `p18_q4_body` | `PBzrpvyyg1wXRRWr-LB4qqlsXsL9dv1dG` | TEXT | "YES. In the original protocol, the attack phase primarily targets glycolysis..." |
| `p18_footer` | `PBzrpvyyg1wXRRWr-LBxyXnQjtZqC2DPP` | TEXT | Footer |

---

## Page 19 — Explanatory Notes (Q4 cont, Q5)

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p19_mechanisms_heading` | `PBzBvbrjH2swz74W-LBNvVvcDS0l9lsTy` | TEXT | "Mechanisms relevant to resistance:" |
| `p19_mechanisms_body` | `PBzBvbrjH2swz74W-LB4Pj1SSKFFHgPKY` | TEXT | "Membrane/lipid raft modulation: DHA and EPA incorporate..." |
| `p19_q5_heading` | `PBzBvbrjH2swz74W-LBlD6m5N9fqbJYXY` | TEXT | "In the Care Oncology Metrics study, doxycycline is given on alternate months with mebendazole. Why?" |
| `p19_q5_body` | `PBzBvbrjH2swz74W-LBGy7Lnkx3SGw2WP` | TEXT | "In the Care Oncology 'Metrics' protocol... I. Different cellular targets... Doxycycline... Mebendazole..." |
| `p19_footer` | `PBzBvbrjH2swz74W-LBjMKFpm8VkwHV2Z` | TEXT | Footer |

---

## Page 20 — Explanatory Notes (Q5 cont, Q6)

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p20_q5_cont` | `PBVrHvvR7MzYNmRg-LBqLyHvQC0JDXYVh` | TEXT | "II. Microbiome and long-term antibiotic stewardship... III. Resistance prevention through evolutionary cycling..." |
| `p20_q6_heading` | `PBVrHvvR7MzYNmRg-LB0YBtX0T7FK9Q3Q` | TEXT | "Should the following phytochemicals be rotated to prevent drug resistance: curcumin, EGCG, sulforaphane, and resveratrol?" |
| `p20_q6_body` | `PBVrHvvR7MzYNmRg-LBwR6j1md72115f1` | TEXT | "NO. For curcumin, EGCG, sulforaphane, and resveratrol, there is no evidence..." |
| `p20_footer` | `PBVrHvvR7MzYNmRg-LB9B9QdHqyh3ZfWD` | TEXT | Footer |

---

## Page 21 — Q6 Continuation

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p21_q6_cont` | `PBQ48hN1BWvCN5xT-LB0HjxPVYFtqGkp2` | TEXT | "These agents are pleiotropic, low-affinity, multitarget modulators..." |
| `p21_footer` | `PBQ48hN1BWvCN5xT-LBsbVZX5f68dZY6Q` | TEXT | Footer |

---

## Page 22 — References

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p22_ref_heading` | `PB2LsqFccnb1vM7J-LB3dn2l2t2yshD4c` | TEXT | "References" |
| `p22_ref_list` | `PB2LsqFccnb1vM7J-LBLVlTJBsl5CP0j7` | TEXT | All 32 references (single large text block) |
| `p22_footer` | `PB2LsqFccnb1vM7J-LB2yPYWkmj7kkz7K` | TEXT | Footer |

---

## Page 23 — Donation CTA

| Slot Name | Element ID | Type | Content Preview |
|-----------|-----------|------|-----------------|
| `p23_background_image` | `PBmq5DL0nFRmfcLF-LBMpQwwLTBvp2PZb` | IMAGE (fill) | Full-page background photo (asset: MAHC6u1Iz8I) — editable |
| `p23_thanks_box_shape` | `PBmq5DL0nFRmfcLF-LBBBFZk4GGycDqcX-LBTD3SSxMP7rr0s0` | SHAPE | Overlay box for "thanks to you" text |
| `p23_thanks_text` | `PBmq5DL0nFRmfcLF-LBBBFZk4GGycDqcX-LB9y5VDTG1mwNzYL` | TEXT | "thanks to you, this 'Cancer-Resistance and Interventions to MItigate ResistancE' guide is free!" |
| `p23_donor_text` | `PBmq5DL0nFRmfcLF-LBBBFZk4GGycDqcX-LBKwBTGH8nsgw7Ky` | TEXT | "We're 100% donor-supported. Your gift enables us to do this critical research..." |
| `p23_donate_box_shape` | `PBmq5DL0nFRmfcLF-LB1D0SPTZ0Cnrz7K-LBvB9XCrJcrBDT4y` | SHAPE | Donate box background |
| `p23_donate_text` | `PBmq5DL0nFRmfcLF-LB1D0SPTZ0Cnrz7K-LBb6ycFVqhLwz42R` | TEXT | "Help make resources like this possible.\nDonate Today!\nIMAhealth.org/donate" |
| `p23_donate_qr` | `PBmq5DL0nFRmfcLF-LB1D0SPTZ0Cnrz7K-LBy6q99xM7tJYSVt` | IMAGE (fill) | QR code for donation (asset: MAGtJ-IZoAY) — editable |
| `p23_ima_footer_logo` | `PBmq5DL0nFRmfcLF-LBLN2xVs4RKMSJLr` | IMAGE (fill) | IMA logo footer (asset: MAGnRWwu6GE) — NOT editable |

---

## Element Totals

- **TEXT elements**: 87
- **IMAGE (fill) elements**: 10
- **SHAPE elements**: 5
- **Pages**: 23

## Footer Pattern

Every page (2-22) has a footer element with:
`"Cancer-Resistance and Interventions to Mitigate Resistance  (03/04/2026)"`

When creating a new guide, all footers must be updated with the new title and date.
Use `find_and_replace_text` with the old footer text to update all at once.

## How to Use This Map

### For a new guide with SAME structure (same number of sections):
1. Duplicate the template in Canva (File → Make a copy)
2. Run `start-editing-transaction` on the copy to get fresh element IDs
3. Match elements by page position and content preview to this slot map
4. Use `replace_text` for each slot with new content
5. Use `find_and_replace_text` for footer updates (bulk)
6. Use `update_fill` for any new figure images

### For a new guide with DIFFERENT structure:
1. Duplicate the template
2. Use `merge-designs` to add/remove pages as needed
3. Follow the same slot-by-slot replacement approach
4. Some slots may need to be emptied or repurposed

### Input format for new guides:
Users should provide content in markdown with slot markers:
```markdown
## SLOT: cover_title_1
NEW TOPIC

## SLOT: cover_title_2
Subtitle Here

## SLOT: cover_subtitle
And Additional Context

## SLOT: intro_body
Full introduction text here...
```
