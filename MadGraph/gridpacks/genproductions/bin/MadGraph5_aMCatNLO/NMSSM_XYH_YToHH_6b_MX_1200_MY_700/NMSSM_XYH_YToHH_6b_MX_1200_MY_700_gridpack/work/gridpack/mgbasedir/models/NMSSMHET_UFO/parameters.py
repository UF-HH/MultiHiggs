# This file was automatically created by FeynRules 2.3.27
# Mathematica version: 9.0 for Linux x86 (64-bit) (November 20, 2012)
# Date: Wed 17 Oct 2018 14:11:01



from object_library import all_parameters, Parameter


from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot

# This is a default parameter object representing 0.
ZERO = Parameter(name = 'ZERO',
                 nature = 'internal',
                 type = 'real',
                 value = '0.0',
                 texname = '0')

# User-defined parameters.
RRd1x3 = Parameter(name = 'RRd1x3',
                   nature = 'external',
                   type = 'real',
                   value = 0.990890455,
                   texname = '\\text{RRd1x3}',
                   lhablock = 'DSQMIX',
                   lhacode = [ 1, 3 ])

RRd1x6 = Parameter(name = 'RRd1x6',
                   nature = 'external',
                   type = 'real',
                   value = 0.134670361,
                   texname = '\\text{RRd1x6}',
                   lhablock = 'DSQMIX',
                   lhacode = [ 1, 6 ])

RRd2x3 = Parameter(name = 'RRd2x3',
                   nature = 'external',
                   type = 'real',
                   value = -0.134670361,
                   texname = '\\text{RRd2x3}',
                   lhablock = 'DSQMIX',
                   lhacode = [ 2, 3 ])

RRd2x6 = Parameter(name = 'RRd2x6',
                   nature = 'external',
                   type = 'real',
                   value = 0.990890455,
                   texname = '\\text{RRd2x6}',
                   lhablock = 'DSQMIX',
                   lhacode = [ 2, 6 ])

RRd3x5 = Parameter(name = 'RRd3x5',
                   nature = 'external',
                   type = 'real',
                   value = 1.,
                   texname = '\\text{RRd3x5}',
                   lhablock = 'DSQMIX',
                   lhacode = [ 3, 5 ])

RRd4x4 = Parameter(name = 'RRd4x4',
                   nature = 'external',
                   type = 'real',
                   value = 1.,
                   texname = '\\text{RRd4x4}',
                   lhablock = 'DSQMIX',
                   lhacode = [ 4, 4 ])

RRd5x1 = Parameter(name = 'RRd5x1',
                   nature = 'external',
                   type = 'real',
                   value = 1.,
                   texname = '\\text{RRd5x1}',
                   lhablock = 'DSQMIX',
                   lhacode = [ 5, 1 ])

RRd6x2 = Parameter(name = 'RRd6x2',
                   nature = 'external',
                   type = 'real',
                   value = 1.,
                   texname = '\\text{RRd6x2}',
                   lhablock = 'DSQMIX',
                   lhacode = [ 6, 2 ])

GAGG = Parameter(name = 'GAGG',
                 nature = 'external',
                 type = 'real',
                 value = 1,
                 texname = 'G_A',
                 lhablock = 'HET',
                 lhacode = [ 1 ])

GAyy = Parameter(name = 'GAyy',
                 nature = 'external',
                 type = 'real',
                 value = 1,
                 texname = 'A_A',
                 lhablock = 'HET',
                 lhacode = [ 2 ])

GHGG = Parameter(name = 'GHGG',
                 nature = 'external',
                 type = 'real',
                 value = 1,
                 texname = 'G_H',
                 lhablock = 'HET',
                 lhacode = [ 3 ])

GHyy = Parameter(name = 'GHyy',
                 nature = 'external',
                 type = 'real',
                 value = 1,
                 texname = 'A_H',
                 lhablock = 'HET',
                 lhacode = [ 4 ])

tb = Parameter(name = 'tb',
               nature = 'external',
               type = 'real',
               value = 10.0004319,
               texname = 't_b',
               lhablock = 'HMIX',
               lhacode = [ 2 ])

MA2 = Parameter(name = 'MA2',
                nature = 'external',
                type = 'real',
                value = 1.04827778e6,
                texname = '\\text{Subsuperscript}[m,A,2]',
                lhablock = 'HMIX',
                lhacode = [ 4 ])

RmD21x1 = Parameter(name = 'RmD21x1',
                    nature = 'external',
                    type = 'real',
                    value = 963545.439,
                    texname = '\\text{RmD21x1}',
                    lhablock = 'MSD2',
                    lhacode = [ 1, 1 ])

RmD22x2 = Parameter(name = 'RmD22x2',
                    nature = 'external',
                    type = 'real',
                    value = 963545.439,
                    texname = '\\text{RmD22x2}',
                    lhablock = 'MSD2',
                    lhacode = [ 2, 2 ])

RmD23x3 = Parameter(name = 'RmD23x3',
                    nature = 'external',
                    type = 'real',
                    value = 933451.834,
                    texname = '\\text{RmD23x3}',
                    lhablock = 'MSD2',
                    lhacode = [ 3, 3 ])

RmE21x1 = Parameter(name = 'RmE21x1',
                    nature = 'external',
                    type = 'real',
                    value = 66311.1508,
                    texname = '\\text{RmE21x1}',
                    lhablock = 'MSE2',
                    lhacode = [ 1, 1 ])

RmE22x2 = Parameter(name = 'RmE22x2',
                    nature = 'external',
                    type = 'real',
                    value = 66311.1508,
                    texname = '\\text{RmE22x2}',
                    lhablock = 'MSE2',
                    lhacode = [ 2, 2 ])

RmE23x3 = Parameter(name = 'RmE23x3',
                    nature = 'external',
                    type = 'real',
                    value = 48897.3735,
                    texname = '\\text{RmE23x3}',
                    lhablock = 'MSE2',
                    lhacode = [ 3, 3 ])

RmL21x1 = Parameter(name = 'RmL21x1',
                    nature = 'external',
                    type = 'real',
                    value = 142415.235,
                    texname = '\\text{RmL21x1}',
                    lhablock = 'MSL2',
                    lhacode = [ 1, 1 ])

RmL22x2 = Parameter(name = 'RmL22x2',
                    nature = 'external',
                    type = 'real',
                    value = 142415.235,
                    texname = '\\text{RmL22x2}',
                    lhablock = 'MSL2',
                    lhacode = [ 2, 2 ])

RmL23x3 = Parameter(name = 'RmL23x3',
                    nature = 'external',
                    type = 'real',
                    value = 133786.42,
                    texname = '\\text{RmL23x3}',
                    lhablock = 'MSL2',
                    lhacode = [ 3, 3 ])

RMx1 = Parameter(name = 'RMx1',
                 nature = 'external',
                 type = 'real',
                 value = 211.618677,
                 texname = '\\text{RMx1}',
                 lhablock = 'MSOFT',
                 lhacode = [ 1 ])

RMx2 = Parameter(name = 'RMx2',
                 nature = 'external',
                 type = 'real',
                 value = 391.864817,
                 texname = '\\text{RMx2}',
                 lhablock = 'MSOFT',
                 lhacode = [ 2 ])

RMx3 = Parameter(name = 'RMx3',
                 nature = 'external',
                 type = 'real',
                 value = 1112.25552,
                 texname = '\\text{RMx3}',
                 lhablock = 'MSOFT',
                 lhacode = [ 3 ])

mHd2 = Parameter(name = 'mHd2',
                 nature = 'external',
                 type = 'real',
                 value = 89988.5262,
                 texname = '\\text{Subsuperscript}\\left[m,H_d,2\\right]',
                 lhablock = 'MSOFT',
                 lhacode = [ 21 ])

mHu2 = Parameter(name = 'mHu2',
                 nature = 'external',
                 type = 'real',
                 value = -908071.077,
                 texname = '\\text{Subsuperscript}\\left[m,H_u,2\\right]',
                 lhablock = 'MSOFT',
                 lhacode = [ 22 ])

RmQ21x1 = Parameter(name = 'RmQ21x1',
                    nature = 'external',
                    type = 'real',
                    value = 1.04878444e6,
                    texname = '\\text{RmQ21x1}',
                    lhablock = 'MSQ2',
                    lhacode = [ 1, 1 ])

RmQ22x2 = Parameter(name = 'RmQ22x2',
                    nature = 'external',
                    type = 'real',
                    value = 1.04878444e6,
                    texname = '\\text{RmQ22x2}',
                    lhablock = 'MSQ2',
                    lhacode = [ 2, 2 ])

RmQ23x3 = Parameter(name = 'RmQ23x3',
                    nature = 'external',
                    type = 'real',
                    value = 715579.339,
                    texname = '\\text{RmQ23x3}',
                    lhablock = 'MSQ2',
                    lhacode = [ 3, 3 ])

RmU21x1 = Parameter(name = 'RmU21x1',
                    nature = 'external',
                    type = 'real',
                    value = 972428.308,
                    texname = '\\text{RmU21x1}',
                    lhablock = 'MSU2',
                    lhacode = [ 1, 1 ])

RmU22x2 = Parameter(name = 'RmU22x2',
                    nature = 'external',
                    type = 'real',
                    value = 972428.308,
                    texname = '\\text{RmU22x2}',
                    lhablock = 'MSU2',
                    lhacode = [ 2, 2 ])

RmU23x3 = Parameter(name = 'RmU23x3',
                    nature = 'external',
                    type = 'real',
                    value = 319484.921,
                    texname = '\\text{RmU23x3}',
                    lhablock = 'MSU2',
                    lhacode = [ 3, 3 ])

UP1x1 = Parameter(name = 'UP1x1',
                  nature = 'external',
                  type = 'real',
                  value = 0.0501258919,
                  texname = '\\text{UP1x1}',
                  lhablock = 'NMAMIX',
                  lhacode = [ 1, 1 ])

UP1x2 = Parameter(name = 'UP1x2',
                  nature = 'external',
                  type = 'real',
                  value = 0.00501258919,
                  texname = '\\text{UP1x2}',
                  lhablock = 'NMAMIX',
                  lhacode = [ 1, 2 ])

UP1x3 = Parameter(name = 'UP1x3',
                  nature = 'external',
                  type = 'real',
                  value = 0.998730328,
                  texname = '\\text{UP1x3}',
                  lhablock = 'NMAMIX',
                  lhacode = [ 1, 3 ])

UP2x1 = Parameter(name = 'UP2x1',
                  nature = 'external',
                  type = 'real',
                  value = 0.99377382,
                  texname = '\\text{UP2x1}',
                  lhablock = 'NMAMIX',
                  lhacode = [ 2, 1 ])

UP2x2 = Parameter(name = 'UP2x2',
                  nature = 'external',
                  type = 'real',
                  value = 0.099377382,
                  texname = '\\text{UP2x2}',
                  lhablock = 'NMAMIX',
                  lhacode = [ 2, 2 ])

UP2x3 = Parameter(name = 'UP2x3',
                  nature = 'external',
                  type = 'real',
                  value = -0.0503758979,
                  texname = '\\text{UP2x3}',
                  lhablock = 'NMAMIX',
                  lhacode = [ 2, 3 ])

US1x1 = Parameter(name = 'US1x1',
                  nature = 'external',
                  type = 'real',
                  value = 0.101230631,
                  texname = '\\text{US1x1}',
                  lhablock = 'NMHMIX',
                  lhacode = [ 1, 1 ])

US1x2 = Parameter(name = 'US1x2',
                  nature = 'external',
                  type = 'real',
                  value = 0.994841811,
                  texname = '\\text{US1x2}',
                  lhablock = 'NMHMIX',
                  lhacode = [ 1, 2 ])

US1x3 = Parameter(name = 'US1x3',
                  nature = 'external',
                  type = 'real',
                  value = -0.00649079704,
                  texname = '\\text{US1x3}',
                  lhablock = 'NMHMIX',
                  lhacode = [ 1, 3 ])

US2x1 = Parameter(name = 'US2x1',
                  nature = 'external',
                  type = 'real',
                  value = 0.994850372,
                  texname = '\\text{US2x1}',
                  lhablock = 'NMHMIX',
                  lhacode = [ 2, 1 ])

US2x2 = Parameter(name = 'US2x2',
                  nature = 'external',
                  type = 'real',
                  value = -0.10119434,
                  texname = '\\text{US2x2}',
                  lhablock = 'NMHMIX',
                  lhacode = [ 2, 2 ])

US2x3 = Parameter(name = 'US2x3',
                  nature = 'external',
                  type = 'real',
                  value = 0.00569588834,
                  texname = '\\text{US2x3}',
                  lhablock = 'NMHMIX',
                  lhacode = [ 2, 3 ])

US3x1 = Parameter(name = 'US3x1',
                  nature = 'external',
                  type = 'real',
                  value = -0.00500967595,
                  texname = '\\text{US3x1}',
                  lhablock = 'NMHMIX',
                  lhacode = [ 3, 1 ])

US3x2 = Parameter(name = 'US3x2',
                  nature = 'external',
                  type = 'real',
                  value = 0.00703397022,
                  texname = '\\text{US3x2}',
                  lhablock = 'NMHMIX',
                  lhacode = [ 3, 2 ])

US3x3 = Parameter(name = 'US3x3',
                  nature = 'external',
                  type = 'real',
                  value = 0.999962713,
                  texname = '\\text{US3x3}',
                  lhablock = 'NMHMIX',
                  lhacode = [ 3, 3 ])

RNN1x1 = Parameter(name = 'RNN1x1',
                   nature = 'external',
                   type = 'real',
                   value = 0.998684518,
                   texname = '\\text{RNN1x1}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 1, 1 ])

RNN1x2 = Parameter(name = 'RNN1x2',
                   nature = 'external',
                   type = 'real',
                   value = -0.00814943871,
                   texname = '\\text{RNN1x2}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 1, 2 ])

RNN1x3 = Parameter(name = 'RNN1x3',
                   nature = 'external',
                   type = 'real',
                   value = 0.0483530815,
                   texname = '\\text{RNN1x3}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 1, 3 ])

RNN1x4 = Parameter(name = 'RNN1x4',
                   nature = 'external',
                   type = 'real',
                   value = -0.0149871707,
                   texname = '\\text{RNN1x4}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 1, 4 ])

RNN1x5 = Parameter(name = 'RNN1x5',
                   nature = 'external',
                   type = 'real',
                   value = 0.000430389009,
                   texname = '\\text{RNN1x5}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 1, 5 ])

RNN2x1 = Parameter(name = 'RNN2x1',
                   nature = 'external',
                   type = 'real',
                   value = 0.0138621789,
                   texname = '\\text{RNN2x1}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 2, 1 ])

RNN2x2 = Parameter(name = 'RNN2x2',
                   nature = 'external',
                   type = 'real',
                   value = 0.993268723,
                   texname = '\\text{RNN2x2}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 2, 2 ])

RNN2x3 = Parameter(name = 'RNN2x3',
                   nature = 'external',
                   type = 'real',
                   value = -0.103118961,
                   texname = '\\text{RNN2x3}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 2, 3 ])

RNN2x4 = Parameter(name = 'RNN2x4',
                   nature = 'external',
                   type = 'real',
                   value = 0.05089756,
                   texname = '\\text{RNN2x4}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 2, 4 ])

RNN2x5 = Parameter(name = 'RNN2x5',
                   nature = 'external',
                   type = 'real',
                   value = -0.00100117257,
                   texname = '\\text{RNN2x5}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 2, 5 ])

RNN3x1 = Parameter(name = 'RNN3x1',
                   nature = 'external',
                   type = 'real',
                   value = -0.0232278855,
                   texname = '\\text{RNN3x1}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 3, 1 ])

RNN3x2 = Parameter(name = 'RNN3x2',
                   nature = 'external',
                   type = 'real',
                   value = 0.037295208,
                   texname = '\\text{RNN3x2}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 3, 2 ])

RNN3x3 = Parameter(name = 'RNN3x3',
                   nature = 'external',
                   type = 'real',
                   value = 0.705297681,
                   texname = '\\text{RNN3x3}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 3, 3 ])

RNN3x4 = Parameter(name = 'RNN3x4',
                   nature = 'external',
                   type = 'real',
                   value = 0.707534724,
                   texname = '\\text{RNN3x4}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 3, 4 ])

RNN3x5 = Parameter(name = 'RNN3x5',
                   nature = 'external',
                   type = 'real',
                   value = 0.00439627968,
                   texname = '\\text{RNN3x5}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 3, 5 ])

RNN4x1 = Parameter(name = 'RNN4x1',
                   nature = 'external',
                   type = 'real',
                   value = 0.0435606237,
                   texname = '\\text{RNN4x1}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 4, 1 ])

RNN4x2 = Parameter(name = 'RNN4x2',
                   nature = 'external',
                   type = 'real',
                   value = -0.109361086,
                   texname = '\\text{RNN4x2}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 4, 2 ])

RNN4x3 = Parameter(name = 'RNN4x3',
                   nature = 'external',
                   type = 'real',
                   value = -0.69963098,
                   texname = '\\text{RNN4x3}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 4, 3 ])

RNN4x4 = Parameter(name = 'RNN4x4',
                   nature = 'external',
                   type = 'real',
                   value = 0.704673803,
                   texname = '\\text{RNN4x4}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 4, 4 ])

RNN4x5 = Parameter(name = 'RNN4x5',
                   nature = 'external',
                   type = 'real',
                   value = -0.00969268004,
                   texname = '\\text{RNN4x5}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 4, 5 ])

RNN5x1 = Parameter(name = 'RNN5x1',
                   nature = 'external',
                   type = 'real',
                   value = 0.000108397267,
                   texname = '\\text{RNN5x1}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 5, 1 ])

RNN5x2 = Parameter(name = 'RNN5x2',
                   nature = 'external',
                   type = 'real',
                   value = -0.000226034288,
                   texname = '\\text{RNN5x2}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 5, 2 ])

RNN5x3 = Parameter(name = 'RNN5x3',
                   nature = 'external',
                   type = 'real',
                   value = -0.0100066083,
                   texname = '\\text{RNN5x3}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 5, 3 ])

RNN5x4 = Parameter(name = 'RNN5x4',
                   nature = 'external',
                   type = 'real',
                   value = 0.00377728091,
                   texname = '\\text{RNN5x4}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 5, 4 ])

RNN5x5 = Parameter(name = 'RNN5x5',
                   nature = 'external',
                   type = 'real',
                   value = 0.999942767,
                   texname = '\\text{RNN5x5}',
                   lhablock = 'NMNMIX',
                   lhacode = [ 5, 5 ])

NMl = Parameter(name = 'NMl',
                nature = 'external',
                type = 'real',
                value = 0.1,
                texname = '\\lambda',
                lhablock = 'NMSSMRUN',
                lhacode = [ 1 ])

NMk = Parameter(name = 'NMk',
                nature = 'external',
                type = 'real',
                value = 0.108910706,
                texname = '\\kappa',
                lhablock = 'NMSSMRUN',
                lhacode = [ 2 ])

NMAl = Parameter(name = 'NMAl',
                 nature = 'external',
                 type = 'real',
                 value = -963.907478,
                 texname = 'A_{\\lambda }',
                 lhablock = 'NMSSMRUN',
                 lhacode = [ 3 ])

NMAk = Parameter(name = 'NMAk',
                 nature = 'external',
                 type = 'real',
                 value = -1.58927119,
                 texname = 'A_{\\kappa }',
                 lhablock = 'NMSSMRUN',
                 lhacode = [ 4 ])

mueff = Parameter(name = 'mueff',
                  nature = 'external',
                  type = 'real',
                  value = 970.86792,
                  texname = '\\mu _{\\text{eff}}',
                  lhablock = 'NMSSMRUN',
                  lhacode = [ 5 ])

MS2 = Parameter(name = 'MS2',
                nature = 'external',
                type = 'real',
                value = -2.23503099e6,
                texname = '\\text{Subsuperscript}[M,S,2]',
                lhablock = 'NMSSMRUN',
                lhacode = [ 10 ])

bb = Parameter(name = 'bb',
               nature = 'external',
               type = 'real',
               value = 1,
               texname = 'b',
               lhablock = 'NMSSMRUN',
               lhacode = [ 12 ])

RRl1x3 = Parameter(name = 'RRl1x3',
                   nature = 'external',
                   type = 'real',
                   value = 0.220980319,
                   texname = '\\text{RRl1x3}',
                   lhablock = 'SELMIX',
                   lhacode = [ 1, 3 ])

RRl1x6 = Parameter(name = 'RRl1x6',
                   nature = 'external',
                   type = 'real',
                   value = 0.975278267,
                   texname = '\\text{RRl1x6}',
                   lhablock = 'SELMIX',
                   lhacode = [ 1, 6 ])

RRl2x4 = Parameter(name = 'RRl2x4',
                   nature = 'external',
                   type = 'real',
                   value = 1.,
                   texname = '\\text{RRl2x4}',
                   lhablock = 'SELMIX',
                   lhacode = [ 2, 4 ])

RRl3x5 = Parameter(name = 'RRl3x5',
                   nature = 'external',
                   type = 'real',
                   value = 1.,
                   texname = '\\text{RRl3x5}',
                   lhablock = 'SELMIX',
                   lhacode = [ 3, 5 ])

RRl4x3 = Parameter(name = 'RRl4x3',
                   nature = 'external',
                   type = 'real',
                   value = -0.975278267,
                   texname = '\\text{RRl4x3}',
                   lhablock = 'SELMIX',
                   lhacode = [ 4, 3 ])

RRl4x6 = Parameter(name = 'RRl4x6',
                   nature = 'external',
                   type = 'real',
                   value = 0.220980319,
                   texname = '\\text{RRl4x6}',
                   lhablock = 'SELMIX',
                   lhacode = [ 4, 6 ])

RRl5x1 = Parameter(name = 'RRl5x1',
                   nature = 'external',
                   type = 'real',
                   value = 1.,
                   texname = '\\text{RRl5x1}',
                   lhablock = 'SELMIX',
                   lhacode = [ 5, 1 ])

RRl6x2 = Parameter(name = 'RRl6x2',
                   nature = 'external',
                   type = 'real',
                   value = 1.,
                   texname = '\\text{RRl6x2}',
                   lhablock = 'SELMIX',
                   lhacode = [ 6, 2 ])

aEWM1 = Parameter(name = 'aEWM1',
                  nature = 'external',
                  type = 'real',
                  value = 127.92,
                  texname = '\\text{Subsuperscript}[\\alpha ,w,-1]',
                  lhablock = 'SMINPUTS',
                  lhacode = [ 1 ])

aS = Parameter(name = 'aS',
               nature = 'external',
               type = 'real',
               value = 0.1172,
               texname = '\\alpha _s',
               lhablock = 'SMINPUTS',
               lhacode = [ 3 ])

RRn1x3 = Parameter(name = 'RRn1x3',
                   nature = 'external',
                   type = 'real',
                   value = 1.,
                   texname = '\\text{RRn1x3}',
                   lhablock = 'SNUMIX',
                   lhacode = [ 1, 3 ])

RRn2x2 = Parameter(name = 'RRn2x2',
                   nature = 'external',
                   type = 'real',
                   value = 1.,
                   texname = '\\text{RRn2x2}',
                   lhablock = 'SNUMIX',
                   lhacode = [ 2, 2 ])

RRn3x1 = Parameter(name = 'RRn3x1',
                   nature = 'external',
                   type = 'real',
                   value = 1.,
                   texname = '\\text{RRn3x1}',
                   lhablock = 'SNUMIX',
                   lhacode = [ 3, 1 ])

Rtd3x3 = Parameter(name = 'Rtd3x3',
                   nature = 'external',
                   type = 'real',
                   value = -342.310014,
                   texname = '\\text{Rtd3x3}',
                   lhablock = 'TD',
                   lhacode = [ 3, 3 ])

Rte3x3 = Parameter(name = 'Rte3x3',
                   nature = 'external',
                   type = 'real',
                   value = -177.121653,
                   texname = '\\text{Rte3x3}',
                   lhablock = 'TE',
                   lhacode = [ 3, 3 ])

Rtu3x3 = Parameter(name = 'Rtu3x3',
                   nature = 'external',
                   type = 'real',
                   value = -1213.64864,
                   texname = '\\text{Rtu3x3}',
                   lhablock = 'TU',
                   lhacode = [ 3, 3 ])

RUU1x1 = Parameter(name = 'RUU1x1',
                   nature = 'external',
                   type = 'real',
                   value = 0.989230572,
                   texname = '\\text{RUU1x1}',
                   lhablock = 'UMIX',
                   lhacode = [ 1, 1 ])

RUU1x2 = Parameter(name = 'RUU1x2',
                   nature = 'external',
                   type = 'real',
                   value = -0.146365554,
                   texname = '\\text{RUU1x2}',
                   lhablock = 'UMIX',
                   lhacode = [ 1, 2 ])

RUU2x1 = Parameter(name = 'RUU2x1',
                   nature = 'external',
                   type = 'real',
                   value = 0.146365554,
                   texname = '\\text{RUU2x1}',
                   lhablock = 'UMIX',
                   lhacode = [ 2, 1 ])

RUU2x2 = Parameter(name = 'RUU2x2',
                   nature = 'external',
                   type = 'real',
                   value = 0.989230572,
                   texname = '\\text{RUU2x2}',
                   lhablock = 'UMIX',
                   lhacode = [ 2, 2 ])

RMNS1x1 = Parameter(name = 'RMNS1x1',
                    nature = 'external',
                    type = 'real',
                    value = 1.,
                    texname = '\\text{RMNS1x1}',
                    lhablock = 'UPMNS',
                    lhacode = [ 1, 1 ])

RMNS2x2 = Parameter(name = 'RMNS2x2',
                    nature = 'external',
                    type = 'real',
                    value = 1.,
                    texname = '\\text{RMNS2x2}',
                    lhablock = 'UPMNS',
                    lhacode = [ 2, 2 ])

RMNS3x3 = Parameter(name = 'RMNS3x3',
                    nature = 'external',
                    type = 'real',
                    value = 1.,
                    texname = '\\text{RMNS3x3}',
                    lhablock = 'UPMNS',
                    lhacode = [ 3, 3 ])

RRu1x3 = Parameter(name = 'RRu1x3',
                   nature = 'external',
                   type = 'real',
                   value = 0.405775656,
                   texname = '\\text{RRu1x3}',
                   lhablock = 'USQMIX',
                   lhacode = [ 1, 3 ])

RRu1x6 = Parameter(name = 'RRu1x6',
                   nature = 'external',
                   type = 'real',
                   value = 0.913972711,
                   texname = '\\text{RRu1x6}',
                   lhablock = 'USQMIX',
                   lhacode = [ 1, 6 ])

RRu2x3 = Parameter(name = 'RRu2x3',
                   nature = 'external',
                   type = 'real',
                   value = -0.913972711,
                   texname = '\\text{RRu2x3}',
                   lhablock = 'USQMIX',
                   lhacode = [ 2, 3 ])

RRu2x6 = Parameter(name = 'RRu2x6',
                   nature = 'external',
                   type = 'real',
                   value = 0.405775656,
                   texname = '\\text{RRu2x6}',
                   lhablock = 'USQMIX',
                   lhacode = [ 2, 6 ])

RRu3x5 = Parameter(name = 'RRu3x5',
                   nature = 'external',
                   type = 'real',
                   value = 1.,
                   texname = '\\text{RRu3x5}',
                   lhablock = 'USQMIX',
                   lhacode = [ 3, 5 ])

RRu4x4 = Parameter(name = 'RRu4x4',
                   nature = 'external',
                   type = 'real',
                   value = 1.,
                   texname = '\\text{RRu4x4}',
                   lhablock = 'USQMIX',
                   lhacode = [ 4, 4 ])

RRu5x1 = Parameter(name = 'RRu5x1',
                   nature = 'external',
                   type = 'real',
                   value = 1.,
                   texname = '\\text{RRu5x1}',
                   lhablock = 'USQMIX',
                   lhacode = [ 5, 1 ])

RRu6x2 = Parameter(name = 'RRu6x2',
                   nature = 'external',
                   type = 'real',
                   value = 1.,
                   texname = '\\text{RRu6x2}',
                   lhablock = 'USQMIX',
                   lhacode = [ 6, 2 ])

RCKM1x1 = Parameter(name = 'RCKM1x1',
                    nature = 'external',
                    type = 'real',
                    value = 1.,
                    texname = '\\text{RCKM1x1}',
                    lhablock = 'VCKM',
                    lhacode = [ 1, 1 ])

RCKM2x2 = Parameter(name = 'RCKM2x2',
                    nature = 'external',
                    type = 'real',
                    value = 1.,
                    texname = '\\text{RCKM2x2}',
                    lhablock = 'VCKM',
                    lhacode = [ 2, 2 ])

RCKM3x3 = Parameter(name = 'RCKM3x3',
                    nature = 'external',
                    type = 'real',
                    value = 1.,
                    texname = '\\text{RCKM3x3}',
                    lhablock = 'VCKM',
                    lhacode = [ 3, 3 ])

RVV1x1 = Parameter(name = 'RVV1x1',
                   nature = 'external',
                   type = 'real',
                   value = 0.997382381,
                   texname = '\\text{RVV1x1}',
                   lhablock = 'VMIX',
                   lhacode = [ 1, 1 ])

RVV1x2 = Parameter(name = 'RVV1x2',
                   nature = 'external',
                   type = 'real',
                   value = -0.0723075752,
                   texname = '\\text{RVV1x2}',
                   lhablock = 'VMIX',
                   lhacode = [ 1, 2 ])

RVV2x1 = Parameter(name = 'RVV2x1',
                   nature = 'external',
                   type = 'real',
                   value = 0.0723075752,
                   texname = '\\text{RVV2x1}',
                   lhablock = 'VMIX',
                   lhacode = [ 2, 1 ])

RVV2x2 = Parameter(name = 'RVV2x2',
                   nature = 'external',
                   type = 'real',
                   value = 0.997382381,
                   texname = '\\text{RVV2x2}',
                   lhablock = 'VMIX',
                   lhacode = [ 2, 2 ])

Ryd2x2 = Parameter(name = 'Ryd2x2',
                   nature = 'external',
                   type = 'real',
                   value = 0.0115453,
                   texname = '\\text{Ryd2x2}',
                   lhablock = 'YD',
                   lhacode = [ 2, 2 ])

Ryd3x3 = Parameter(name = 'Ryd3x3',
                   nature = 'external',
                   type = 'real',
                   value = 0.243259,
                   texname = '\\text{Ryd3x3}',
                   lhablock = 'YD',
                   lhacode = [ 3, 3 ])

Rye1x1 = Parameter(name = 'Rye1x1',
                   nature = 'external',
                   type = 'real',
                   value = 0.0000294982,
                   texname = '\\text{Rye1x1}',
                   lhablock = 'YE',
                   lhacode = [ 1, 1 ])

Rye2x2 = Parameter(name = 'Rye2x2',
                   nature = 'external',
                   type = 'real',
                   value = 0.00609591,
                   texname = '\\text{Rye2x2}',
                   lhablock = 'YE',
                   lhacode = [ 2, 2 ])

Rye3x3 = Parameter(name = 'Rye3x3',
                   nature = 'external',
                   type = 'real',
                   value = 0.10258,
                   texname = '\\text{Rye3x3}',
                   lhablock = 'YE',
                   lhacode = [ 3, 3 ])

Ryu2x2 = Parameter(name = 'Ryu2x2',
                   nature = 'external',
                   type = 'real',
                   value = 0.00710004,
                   texname = '\\text{Ryu2x2}',
                   lhablock = 'YU',
                   lhacode = [ 2, 2 ])

Ryu3x3 = Parameter(name = 'Ryu3x3',
                   nature = 'external',
                   type = 'real',
                   value = 0.989388,
                   texname = '\\text{Ryu3x3}',
                   lhablock = 'YU',
                   lhacode = [ 3, 3 ])

MZ = Parameter(name = 'MZ',
               nature = 'external',
               type = 'real',
               value = 91.187,
               texname = '\\text{MZ}',
               lhablock = 'MASS',
               lhacode = [ 23 ])

MW = Parameter(name = 'MW',
               nature = 'external',
               type = 'real',
               value = 80.9387517,
               texname = '\\text{MW}',
               lhablock = 'MASS',
               lhacode = [ 24 ])

Mneu1 = Parameter(name = 'Mneu1',
                  nature = 'external',
                  type = 'real',
                  value = 208.141578,
                  texname = '\\text{Mneu1}',
                  lhablock = 'MASS',
                  lhacode = [ 1000022 ])

Mneu2 = Parameter(name = 'Mneu2',
                  nature = 'external',
                  type = 'real',
                  value = 397.851055,
                  texname = '\\text{Mneu2}',
                  lhablock = 'MASS',
                  lhacode = [ 1000023 ])

Mneu3 = Parameter(name = 'Mneu3',
                  nature = 'external',
                  type = 'real',
                  value = -963.980547,
                  texname = '\\text{Mneu3}',
                  lhablock = 'MASS',
                  lhacode = [ 1000025 ])

Mneu4 = Parameter(name = 'Mneu4',
                  nature = 'external',
                  type = 'real',
                  value = 969.59391,
                  texname = '\\text{Mneu4}',
                  lhablock = 'MASS',
                  lhacode = [ 1000035 ])

Mneu5 = Parameter(name = 'Mneu5',
                  nature = 'external',
                  type = 'real',
                  value = 2094.27413,
                  texname = '\\text{Mneu5}',
                  lhablock = 'MASS',
                  lhacode = [ 1000045 ])

Mch1 = Parameter(name = 'Mch1',
                 nature = 'external',
                 type = 'real',
                 value = 397.829545,
                 texname = '\\text{Mch1}',
                 lhablock = 'MASS',
                 lhacode = [ 1000024 ])

Mch2 = Parameter(name = 'Mch2',
                 nature = 'external',
                 type = 'real',
                 value = 970.136817,
                 texname = '\\text{Mch2}',
                 lhablock = 'MASS',
                 lhacode = [ 1000037 ])

Mgo = Parameter(name = 'Mgo',
                nature = 'external',
                type = 'real',
                value = 1151.54279,
                texname = '\\text{Mgo}',
                lhablock = 'MASS',
                lhacode = [ 1000021 ])

MH01 = Parameter(name = 'MH01',
                 nature = 'external',
                 type = 'real',
                 value = 119.163922,
                 texname = '\\text{MH01}',
                 lhablock = 'MASS',
                 lhacode = [ 25 ])

MH02 = Parameter(name = 'MH02',
                 nature = 'external',
                 type = 'real',
                 value = 1016.55127,
                 texname = '\\text{MH02}',
                 lhablock = 'MASS',
                 lhacode = [ 35 ])

MH03 = Parameter(name = 'MH03',
                 nature = 'external',
                 type = 'real',
                 value = 2112.57647,
                 texname = '\\text{MH03}',
                 lhablock = 'MASS',
                 lhacode = [ 45 ])

MA01 = Parameter(name = 'MA01',
                 nature = 'external',
                 type = 'real',
                 value = 40.3976968,
                 texname = '\\text{MA01}',
                 lhablock = 'MASS',
                 lhacode = [ 36 ])

MA02 = Parameter(name = 'MA02',
                 nature = 'external',
                 type = 'real',
                 value = 1021.04211,
                 texname = '\\text{MA02}',
                 lhablock = 'MASS',
                 lhacode = [ 46 ])

MH = Parameter(name = 'MH',
               nature = 'external',
               type = 'real',
               value = 1022.47183,
               texname = '\\text{MH}',
               lhablock = 'MASS',
               lhacode = [ 37 ])

Me = Parameter(name = 'Me',
               nature = 'external',
               type = 'real',
               value = 0.000511,
               texname = '\\text{Me}',
               lhablock = 'MASS',
               lhacode = [ 11 ])

Mm = Parameter(name = 'Mm',
               nature = 'external',
               type = 'real',
               value = 0.1056,
               texname = '\\text{Mm}',
               lhablock = 'MASS',
               lhacode = [ 13 ])

Mta = Parameter(name = 'Mta',
                nature = 'external',
                type = 'real',
                value = 1.777,
                texname = '\\text{Mta}',
                lhablock = 'MASS',
                lhacode = [ 15 ])

MC = Parameter(name = 'MC',
               nature = 'external',
               type = 'real',
               value = 1.23,
               texname = '\\text{MC}',
               lhablock = 'MASS',
               lhacode = [ 4 ])

MT = Parameter(name = 'MT',
               nature = 'external',
               type = 'real',
               value = 171.4,
               texname = '\\text{MT}',
               lhablock = 'MASS',
               lhacode = [ 6 ])

MS = Parameter(name = 'MS',
               nature = 'external',
               type = 'real',
               value = 0.2,
               texname = '\\text{MS}',
               lhablock = 'MASS',
               lhacode = [ 3 ])

MB = Parameter(name = 'MB',
               nature = 'external',
               type = 'real',
               value = 4.214,
               texname = '\\text{MB}',
               lhablock = 'MASS',
               lhacode = [ 5 ])

Msn1 = Parameter(name = 'Msn1',
                 nature = 'external',
                 type = 'real',
                 value = 360.340595,
                 texname = '\\text{Msn1}',
                 lhablock = 'MASS',
                 lhacode = [ 1000012 ])

Msn2 = Parameter(name = 'Msn2',
                 nature = 'external',
                 type = 'real',
                 value = 372.121162,
                 texname = '\\text{Msn2}',
                 lhablock = 'MASS',
                 lhacode = [ 1000014 ])

Msn3 = Parameter(name = 'Msn3',
                 nature = 'external',
                 type = 'real',
                 value = 372.121162,
                 texname = '\\text{Msn3}',
                 lhablock = 'MASS',
                 lhacode = [ 1000016 ])

Msl1 = Parameter(name = 'Msl1',
                 nature = 'external',
                 type = 'real',
                 value = 214.739576,
                 texname = '\\text{Msl1}',
                 lhablock = 'MASS',
                 lhacode = [ 1000011 ])

Msl2 = Parameter(name = 'Msl2',
                 nature = 'external',
                 type = 'real',
                 value = 261.024365,
                 texname = '\\text{Msl2}',
                 lhablock = 'MASS',
                 lhacode = [ 1000013 ])

Msl3 = Parameter(name = 'Msl3',
                 nature = 'external',
                 type = 'real',
                 value = 261.024365,
                 texname = '\\text{Msl3}',
                 lhablock = 'MASS',
                 lhacode = [ 1000015 ])

Msl4 = Parameter(name = 'Msl4',
                 nature = 'external',
                 type = 'real',
                 value = 374.857439,
                 texname = '\\text{Msl4}',
                 lhablock = 'MASS',
                 lhacode = [ 2000011 ])

Msl5 = Parameter(name = 'Msl5',
                 nature = 'external',
                 type = 'real',
                 value = 380.175937,
                 texname = '\\text{Msl5}',
                 lhablock = 'MASS',
                 lhacode = [ 2000013 ])

Msl6 = Parameter(name = 'Msl6',
                 nature = 'external',
                 type = 'real',
                 value = 380.175937,
                 texname = '\\text{Msl6}',
                 lhablock = 'MASS',
                 lhacode = [ 2000015 ])

Msu1 = Parameter(name = 'Msu1',
                 nature = 'external',
                 type = 'real',
                 value = 499.229271,
                 texname = '\\text{Msu1}',
                 lhablock = 'MASS',
                 lhacode = [ 1000002 ])

Msu2 = Parameter(name = 'Msu2',
                 nature = 'external',
                 type = 'real',
                 value = 935.527355,
                 texname = '\\text{Msu2}',
                 lhablock = 'MASS',
                 lhacode = [ 1000004 ])

Msu3 = Parameter(name = 'Msu3',
                 nature = 'external',
                 type = 'real',
                 value = 1027.25889,
                 texname = '\\text{Msu3}',
                 lhablock = 'MASS',
                 lhacode = [ 1000006 ])

Msu4 = Parameter(name = 'Msu4',
                 nature = 'external',
                 type = 'real',
                 value = 1027.25889,
                 texname = '\\text{Msu4}',
                 lhablock = 'MASS',
                 lhacode = [ 2000002 ])

Msu5 = Parameter(name = 'Msu5',
                 nature = 'external',
                 type = 'real',
                 value = 1063.63463,
                 texname = '\\text{Msu5}',
                 lhablock = 'MASS',
                 lhacode = [ 2000004 ])

Msu6 = Parameter(name = 'Msu6',
                 nature = 'external',
                 type = 'real',
                 value = 1063.63463,
                 texname = '\\text{Msu6}',
                 lhablock = 'MASS',
                 lhacode = [ 2000006 ])

Msd1 = Parameter(name = 'Msd1',
                 nature = 'external',
                 type = 'real',
                 value = 866.365161,
                 texname = '\\text{Msd1}',
                 lhablock = 'MASS',
                 lhacode = [ 1000001 ])

Msd2 = Parameter(name = 'Msd2',
                 nature = 'external',
                 type = 'real',
                 value = 992.138103,
                 texname = '\\text{Msd2}',
                 lhablock = 'MASS',
                 lhacode = [ 1000003 ])

Msd3 = Parameter(name = 'Msd3',
                 nature = 'external',
                 type = 'real',
                 value = 1023.75369,
                 texname = '\\text{Msd3}',
                 lhablock = 'MASS',
                 lhacode = [ 1000005 ])

Msd4 = Parameter(name = 'Msd4',
                 nature = 'external',
                 type = 'real',
                 value = 1023.75369,
                 texname = '\\text{Msd4}',
                 lhablock = 'MASS',
                 lhacode = [ 2000001 ])

Msd5 = Parameter(name = 'Msd5',
                 nature = 'external',
                 type = 'real',
                 value = 1066.51941,
                 texname = '\\text{Msd5}',
                 lhablock = 'MASS',
                 lhacode = [ 2000003 ])

Msd6 = Parameter(name = 'Msd6',
                 nature = 'external',
                 type = 'real',
                 value = 1066.51941,
                 texname = '\\text{Msd6}',
                 lhablock = 'MASS',
                 lhacode = [ 2000005 ])

Wneu2 = Parameter(name = 'Wneu2',
                  nature = 'external',
                  type = 'real',
                  value = 2.,
                  texname = '\\text{Wneu2}',
                  lhablock = 'DECAY',
                  lhacode = [ 1000023 ])

Wneu3 = Parameter(name = 'Wneu3',
                  nature = 'external',
                  type = 'real',
                  value = 2.,
                  texname = '\\text{Wneu3}',
                  lhablock = 'DECAY',
                  lhacode = [ 1000025 ])

Wneu4 = Parameter(name = 'Wneu4',
                  nature = 'external',
                  type = 'real',
                  value = 2.,
                  texname = '\\text{Wneu4}',
                  lhablock = 'DECAY',
                  lhacode = [ 1000035 ])

Wneu5 = Parameter(name = 'Wneu5',
                  nature = 'external',
                  type = 'real',
                  value = 2.,
                  texname = '\\text{Wneu5}',
                  lhablock = 'DECAY',
                  lhacode = [ 1000045 ])

Wch1 = Parameter(name = 'Wch1',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wch1}',
                 lhablock = 'DECAY',
                 lhacode = [ 1000024 ])

Wch2 = Parameter(name = 'Wch2',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wch2}',
                 lhablock = 'DECAY',
                 lhacode = [ 1000037 ])

Wgo = Parameter(name = 'Wgo',
                nature = 'external',
                type = 'real',
                value = 2.,
                texname = '\\text{Wgo}',
                lhablock = 'DECAY',
                lhacode = [ 1000021 ])

WH01 = Parameter(name = 'WH01',
                 nature = 'external',
                 type = 'real',
                 value = 0.0303786329,
                 texname = '\\text{WH01}',
                 lhablock = 'DECAY',
                 lhacode = [ 25 ])

WH02 = Parameter(name = 'WH02',
                 nature = 'external',
                 type = 'real',
                 value = 4.9565785,
                 texname = '\\text{WH02}',
                 lhablock = 'DECAY',
                 lhacode = [ 35 ])

WH03 = Parameter(name = 'WH03',
                 nature = 'external',
                 type = 'real',
                 value = 1.11808339,
                 texname = '\\text{WH03}',
                 lhablock = 'DECAY',
                 lhacode = [ 45 ])

WA01 = Parameter(name = 'WA01',
                 nature = 'external',
                 type = 'real',
                 value = 0.000249558656,
                 texname = '\\text{WA01}',
                 lhablock = 'DECAY',
                 lhacode = [ 36 ])

WA02 = Parameter(name = 'WA02',
                 nature = 'external',
                 type = 'real',
                 value = 3.50947871,
                 texname = '\\text{WA02}',
                 lhablock = 'DECAY',
                 lhacode = [ 46 ])

WH = Parameter(name = 'WH',
               nature = 'external',
               type = 'real',
               value = 3.25001093,
               texname = '\\text{WH}',
               lhablock = 'DECAY',
               lhacode = [ 37 ])

WT = Parameter(name = 'WT',
               nature = 'external',
               type = 'real',
               value = 1.33482521,
               texname = '\\text{WT}',
               lhablock = 'DECAY',
               lhacode = [ 6 ])

Wsn1 = Parameter(name = 'Wsn1',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsn1}',
                 lhablock = 'DECAY',
                 lhacode = [ 1000012 ])

Wsn2 = Parameter(name = 'Wsn2',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsn2}',
                 lhablock = 'DECAY',
                 lhacode = [ 1000014 ])

Wsn3 = Parameter(name = 'Wsn3',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsn3}',
                 lhablock = 'DECAY',
                 lhacode = [ 1000016 ])

Wsl1 = Parameter(name = 'Wsl1',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsl1}',
                 lhablock = 'DECAY',
                 lhacode = [ 1000011 ])

Wsl2 = Parameter(name = 'Wsl2',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsl2}',
                 lhablock = 'DECAY',
                 lhacode = [ 1000013 ])

Wsl3 = Parameter(name = 'Wsl3',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsl3}',
                 lhablock = 'DECAY',
                 lhacode = [ 1000015 ])

Wsl4 = Parameter(name = 'Wsl4',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsl4}',
                 lhablock = 'DECAY',
                 lhacode = [ 2000011 ])

Wsl5 = Parameter(name = 'Wsl5',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsl5}',
                 lhablock = 'DECAY',
                 lhacode = [ 2000013 ])

Wsl6 = Parameter(name = 'Wsl6',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsl6}',
                 lhablock = 'DECAY',
                 lhacode = [ 2000015 ])

Wsu1 = Parameter(name = 'Wsu1',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsu1}',
                 lhablock = 'DECAY',
                 lhacode = [ 1000002 ])

Wsu2 = Parameter(name = 'Wsu2',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsu2}',
                 lhablock = 'DECAY',
                 lhacode = [ 1000004 ])

Wsu3 = Parameter(name = 'Wsu3',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsu3}',
                 lhablock = 'DECAY',
                 lhacode = [ 1000006 ])

Wsu4 = Parameter(name = 'Wsu4',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsu4}',
                 lhablock = 'DECAY',
                 lhacode = [ 2000002 ])

Wsu5 = Parameter(name = 'Wsu5',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsu5}',
                 lhablock = 'DECAY',
                 lhacode = [ 2000004 ])

Wsu6 = Parameter(name = 'Wsu6',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsu6}',
                 lhablock = 'DECAY',
                 lhacode = [ 2000006 ])

Wsd1 = Parameter(name = 'Wsd1',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsd1}',
                 lhablock = 'DECAY',
                 lhacode = [ 1000001 ])

Wsd2 = Parameter(name = 'Wsd2',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsd2}',
                 lhablock = 'DECAY',
                 lhacode = [ 1000003 ])

Wsd3 = Parameter(name = 'Wsd3',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsd3}',
                 lhablock = 'DECAY',
                 lhacode = [ 1000005 ])

Wsd4 = Parameter(name = 'Wsd4',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsd4}',
                 lhablock = 'DECAY',
                 lhacode = [ 2000001 ])

Wsd5 = Parameter(name = 'Wsd5',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsd5}',
                 lhablock = 'DECAY',
                 lhacode = [ 2000003 ])

Wsd6 = Parameter(name = 'Wsd6',
                 nature = 'external',
                 type = 'real',
                 value = 2.,
                 texname = '\\text{Wsd6}',
                 lhablock = 'DECAY',
                 lhacode = [ 2000005 ])

beta = Parameter(name = 'beta',
                 nature = 'internal',
                 type = 'real',
                 value = 'cmath.atan(tb)',
                 texname = '\\beta')

cw = Parameter(name = 'cw',
               nature = 'internal',
               type = 'real',
               value = 'MW/MZ',
               texname = 'c_w')

mD21x1 = Parameter(name = 'mD21x1',
                   nature = 'internal',
                   type = 'complex',
                   value = 'RmD21x1',
                   texname = '\\text{mD21x1}')

mD22x2 = Parameter(name = 'mD22x2',
                   nature = 'internal',
                   type = 'complex',
                   value = 'RmD22x2',
                   texname = '\\text{mD22x2}')

mD23x3 = Parameter(name = 'mD23x3',
                   nature = 'internal',
                   type = 'complex',
                   value = 'RmD23x3',
                   texname = '\\text{mD23x3}')

mE21x1 = Parameter(name = 'mE21x1',
                   nature = 'internal',
                   type = 'complex',
                   value = 'RmE21x1',
                   texname = '\\text{mE21x1}')

mE22x2 = Parameter(name = 'mE22x2',
                   nature = 'internal',
                   type = 'complex',
                   value = 'RmE22x2',
                   texname = '\\text{mE22x2}')

mE23x3 = Parameter(name = 'mE23x3',
                   nature = 'internal',
                   type = 'complex',
                   value = 'RmE23x3',
                   texname = '\\text{mE23x3}')

mL21x1 = Parameter(name = 'mL21x1',
                   nature = 'internal',
                   type = 'complex',
                   value = 'RmL21x1',
                   texname = '\\text{mL21x1}')

mL22x2 = Parameter(name = 'mL22x2',
                   nature = 'internal',
                   type = 'complex',
                   value = 'RmL22x2',
                   texname = '\\text{mL22x2}')

mL23x3 = Parameter(name = 'mL23x3',
                   nature = 'internal',
                   type = 'complex',
                   value = 'RmL23x3',
                   texname = '\\text{mL23x3}')

mQ21x1 = Parameter(name = 'mQ21x1',
                   nature = 'internal',
                   type = 'complex',
                   value = 'RmQ21x1',
                   texname = '\\text{mQ21x1}')

mQ22x2 = Parameter(name = 'mQ22x2',
                   nature = 'internal',
                   type = 'complex',
                   value = 'RmQ22x2',
                   texname = '\\text{mQ22x2}')

mQ23x3 = Parameter(name = 'mQ23x3',
                   nature = 'internal',
                   type = 'complex',
                   value = 'RmQ23x3',
                   texname = '\\text{mQ23x3}')

mU21x1 = Parameter(name = 'mU21x1',
                   nature = 'internal',
                   type = 'complex',
                   value = 'RmU21x1',
                   texname = '\\text{mU21x1}')

mU22x2 = Parameter(name = 'mU22x2',
                   nature = 'internal',
                   type = 'complex',
                   value = 'RmU22x2',
                   texname = '\\text{mU22x2}')

mU23x3 = Parameter(name = 'mU23x3',
                   nature = 'internal',
                   type = 'complex',
                   value = 'RmU23x3',
                   texname = '\\text{mU23x3}')

Mx1 = Parameter(name = 'Mx1',
                nature = 'internal',
                type = 'complex',
                value = 'RMx1',
                texname = 'M_1')

Mx2 = Parameter(name = 'Mx2',
                nature = 'internal',
                type = 'complex',
                value = 'RMx2',
                texname = 'M_2')

Mx3 = Parameter(name = 'Mx3',
                nature = 'internal',
                type = 'complex',
                value = 'RMx3',
                texname = 'M_3')

NN1x1 = Parameter(name = 'NN1x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN1x1',
                  texname = '\\text{NN1x1}')

NN1x2 = Parameter(name = 'NN1x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN1x2',
                  texname = '\\text{NN1x2}')

NN1x3 = Parameter(name = 'NN1x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN1x3',
                  texname = '\\text{NN1x3}')

NN1x4 = Parameter(name = 'NN1x4',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN1x4',
                  texname = '\\text{NN1x4}')

NN1x5 = Parameter(name = 'NN1x5',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN1x5',
                  texname = '\\text{NN1x5}')

NN2x1 = Parameter(name = 'NN2x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN2x1',
                  texname = '\\text{NN2x1}')

NN2x2 = Parameter(name = 'NN2x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN2x2',
                  texname = '\\text{NN2x2}')

NN2x3 = Parameter(name = 'NN2x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN2x3',
                  texname = '\\text{NN2x3}')

NN2x4 = Parameter(name = 'NN2x4',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN2x4',
                  texname = '\\text{NN2x4}')

NN2x5 = Parameter(name = 'NN2x5',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN2x5',
                  texname = '\\text{NN2x5}')

NN3x1 = Parameter(name = 'NN3x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN3x1',
                  texname = '\\text{NN3x1}')

NN3x2 = Parameter(name = 'NN3x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN3x2',
                  texname = '\\text{NN3x2}')

NN3x3 = Parameter(name = 'NN3x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN3x3',
                  texname = '\\text{NN3x3}')

NN3x4 = Parameter(name = 'NN3x4',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN3x4',
                  texname = '\\text{NN3x4}')

NN3x5 = Parameter(name = 'NN3x5',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN3x5',
                  texname = '\\text{NN3x5}')

NN4x1 = Parameter(name = 'NN4x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN4x1',
                  texname = '\\text{NN4x1}')

NN4x2 = Parameter(name = 'NN4x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN4x2',
                  texname = '\\text{NN4x2}')

NN4x3 = Parameter(name = 'NN4x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN4x3',
                  texname = '\\text{NN4x3}')

NN4x4 = Parameter(name = 'NN4x4',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN4x4',
                  texname = '\\text{NN4x4}')

NN4x5 = Parameter(name = 'NN4x5',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN4x5',
                  texname = '\\text{NN4x5}')

NN5x1 = Parameter(name = 'NN5x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN5x1',
                  texname = '\\text{NN5x1}')

NN5x2 = Parameter(name = 'NN5x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN5x2',
                  texname = '\\text{NN5x2}')

NN5x3 = Parameter(name = 'NN5x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN5x3',
                  texname = '\\text{NN5x3}')

NN5x4 = Parameter(name = 'NN5x4',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN5x4',
                  texname = '\\text{NN5x4}')

NN5x5 = Parameter(name = 'NN5x5',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RNN5x5',
                  texname = '\\text{NN5x5}')

Rd1x3 = Parameter(name = 'Rd1x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRd1x3',
                  texname = '\\text{Rd1x3}')

Rd1x6 = Parameter(name = 'Rd1x6',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRd1x6',
                  texname = '\\text{Rd1x6}')

Rd2x3 = Parameter(name = 'Rd2x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRd2x3',
                  texname = '\\text{Rd2x3}')

Rd2x6 = Parameter(name = 'Rd2x6',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRd2x6',
                  texname = '\\text{Rd2x6}')

Rd3x5 = Parameter(name = 'Rd3x5',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRd3x5',
                  texname = '\\text{Rd3x5}')

Rd4x4 = Parameter(name = 'Rd4x4',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRd4x4',
                  texname = '\\text{Rd4x4}')

Rd5x1 = Parameter(name = 'Rd5x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRd5x1',
                  texname = '\\text{Rd5x1}')

Rd6x2 = Parameter(name = 'Rd6x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRd6x2',
                  texname = '\\text{Rd6x2}')

Rl1x3 = Parameter(name = 'Rl1x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRl1x3',
                  texname = '\\text{Rl1x3}')

Rl1x6 = Parameter(name = 'Rl1x6',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRl1x6',
                  texname = '\\text{Rl1x6}')

Rl2x4 = Parameter(name = 'Rl2x4',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRl2x4',
                  texname = '\\text{Rl2x4}')

Rl3x5 = Parameter(name = 'Rl3x5',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRl3x5',
                  texname = '\\text{Rl3x5}')

Rl4x3 = Parameter(name = 'Rl4x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRl4x3',
                  texname = '\\text{Rl4x3}')

Rl4x6 = Parameter(name = 'Rl4x6',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRl4x6',
                  texname = '\\text{Rl4x6}')

Rl5x1 = Parameter(name = 'Rl5x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRl5x1',
                  texname = '\\text{Rl5x1}')

Rl6x2 = Parameter(name = 'Rl6x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRl6x2',
                  texname = '\\text{Rl6x2}')

Rn1x3 = Parameter(name = 'Rn1x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRn1x3',
                  texname = '\\text{Rn1x3}')

Rn2x2 = Parameter(name = 'Rn2x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRn2x2',
                  texname = '\\text{Rn2x2}')

Rn3x1 = Parameter(name = 'Rn3x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRn3x1',
                  texname = '\\text{Rn3x1}')

Ru1x3 = Parameter(name = 'Ru1x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRu1x3',
                  texname = '\\text{Ru1x3}')

Ru1x6 = Parameter(name = 'Ru1x6',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRu1x6',
                  texname = '\\text{Ru1x6}')

Ru2x3 = Parameter(name = 'Ru2x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRu2x3',
                  texname = '\\text{Ru2x3}')

Ru2x6 = Parameter(name = 'Ru2x6',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRu2x6',
                  texname = '\\text{Ru2x6}')

Ru3x5 = Parameter(name = 'Ru3x5',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRu3x5',
                  texname = '\\text{Ru3x5}')

Ru4x4 = Parameter(name = 'Ru4x4',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRu4x4',
                  texname = '\\text{Ru4x4}')

Ru5x1 = Parameter(name = 'Ru5x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRu5x1',
                  texname = '\\text{Ru5x1}')

Ru6x2 = Parameter(name = 'Ru6x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RRu6x2',
                  texname = '\\text{Ru6x2}')

UP31 = Parameter(name = 'UP31',
                 nature = 'internal',
                 type = 'real',
                 value = 'cmath.sqrt(1 - UP1x1**2 - UP2x1**2)',
                 texname = '\\text{Subsuperscript}[U,P,31]')

UP32 = Parameter(name = 'UP32',
                 nature = 'internal',
                 type = 'real',
                 value = 'cmath.sqrt(1 - UP1x2**2 - UP2x2**2)',
                 texname = '\\text{Subsuperscript}[U,P,32]')

UP33 = Parameter(name = 'UP33',
                 nature = 'internal',
                 type = 'real',
                 value = 'cmath.sqrt(1 - UP1x3**2 - UP2x3**2)',
                 texname = '\\text{Subsuperscript}[U,P,33]')

UU1x1 = Parameter(name = 'UU1x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RUU1x1',
                  texname = '\\text{UU1x1}')

UU1x2 = Parameter(name = 'UU1x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RUU1x2',
                  texname = '\\text{UU1x2}')

UU2x1 = Parameter(name = 'UU2x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RUU2x1',
                  texname = '\\text{UU2x1}')

UU2x2 = Parameter(name = 'UU2x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RUU2x2',
                  texname = '\\text{UU2x2}')

vs = Parameter(name = 'vs',
               nature = 'internal',
               type = 'real',
               value = '(mueff*cmath.sqrt(2))/NMl',
               texname = 'v_s')

VV1x1 = Parameter(name = 'VV1x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RVV1x1',
                  texname = '\\text{VV1x1}')

VV1x2 = Parameter(name = 'VV1x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RVV1x2',
                  texname = '\\text{VV1x2}')

VV2x1 = Parameter(name = 'VV2x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RVV2x1',
                  texname = '\\text{VV2x1}')

VV2x2 = Parameter(name = 'VV2x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'RVV2x2',
                  texname = '\\text{VV2x2}')

ee = Parameter(name = 'ee',
               nature = 'internal',
               type = 'real',
               value = '2*cmath.sqrt(1/aEWM1)*cmath.sqrt(cmath.pi)',
               texname = 'e')

G = Parameter(name = 'G',
              nature = 'internal',
              type = 'real',
              value = '2*cmath.sqrt(aS)*cmath.sqrt(cmath.pi)',
              texname = 'G')

td3x3 = Parameter(name = 'td3x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rtd3x3',
                  texname = '\\text{td3x3}')

te3x3 = Parameter(name = 'te3x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rte3x3',
                  texname = '\\text{te3x3}')

tu3x3 = Parameter(name = 'tu3x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rtu3x3',
                  texname = '\\text{tu3x3}')

yd2x2 = Parameter(name = 'yd2x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Ryd2x2',
                  texname = '\\text{yd2x2}')

yd3x3 = Parameter(name = 'yd3x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Ryd3x3',
                  texname = '\\text{yd3x3}')

ye1x1 = Parameter(name = 'ye1x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rye1x1',
                  texname = '\\text{ye1x1}')

ye2x2 = Parameter(name = 'ye2x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rye2x2',
                  texname = '\\text{ye2x2}')

ye3x3 = Parameter(name = 'ye3x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rye3x3',
                  texname = '\\text{ye3x3}')

yu2x2 = Parameter(name = 'yu2x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Ryu2x2',
                  texname = '\\text{yu2x2}')

yu3x3 = Parameter(name = 'yu3x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Ryu3x3',
                  texname = '\\text{yu3x3}')

sw = Parameter(name = 'sw',
               nature = 'internal',
               type = 'real',
               value = 'cmath.sqrt(1 - cw**2)',
               texname = 's_w')

gp = Parameter(name = 'gp',
               nature = 'internal',
               type = 'real',
               value = 'ee/cw',
               texname = 'g\'')

gw = Parameter(name = 'gw',
               nature = 'internal',
               type = 'real',
               value = 'ee/sw',
               texname = 'g_w')

vev = Parameter(name = 'vev',
                nature = 'internal',
                type = 'real',
                value = '(2*cw*MZ*sw)/ee',
                texname = 'v')

vd = Parameter(name = 'vd',
               nature = 'internal',
               type = 'real',
               value = 'vev*cmath.cos(beta)',
               texname = 'v_d')

vu = Parameter(name = 'vu',
               nature = 'internal',
               type = 'real',
               value = 'vev*cmath.sin(beta)',
               texname = 'v_u')

I1a22 = Parameter(name = 'I1a22',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complexconjugate(yu2x2)',
                  texname = '\\text{I1a22}')

I1a33 = Parameter(name = 'I1a33',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complexconjugate(yu3x3)',
                  texname = '\\text{I1a33}')

I10a26 = Parameter(name = 'I10a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd6x2*complexconjugate(yu2x2)',
                   texname = '\\text{I10a26}')

I10a31 = Parameter(name = 'I10a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(yu3x3)',
                   texname = '\\text{I10a31}')

I10a32 = Parameter(name = 'I10a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(yu3x3)',
                   texname = '\\text{I10a32}')

I100a11 = Parameter(name = 'I100a11',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Rd1x6*complexconjugate(Rd1x6)',
                    texname = '\\text{I100a11}')

I100a12 = Parameter(name = 'I100a12',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Rd2x6*complexconjugate(Rd1x6)',
                    texname = '\\text{I100a12}')

I100a21 = Parameter(name = 'I100a21',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Rd1x6*complexconjugate(Rd2x6)',
                    texname = '\\text{I100a21}')

I100a22 = Parameter(name = 'I100a22',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Rd2x6*complexconjugate(Rd2x6)',
                    texname = '\\text{I100a22}')

I100a33 = Parameter(name = 'I100a33',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Rd3x5*complexconjugate(Rd3x5)',
                    texname = '\\text{I100a33}')

I100a44 = Parameter(name = 'I100a44',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Rd4x4*complexconjugate(Rd4x4)',
                    texname = '\\text{I100a44}')

I101a11 = Parameter(name = 'I101a11',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Rl1x6*complexconjugate(Rl1x6)',
                    texname = '\\text{I101a11}')

I101a14 = Parameter(name = 'I101a14',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Rl4x6*complexconjugate(Rl1x6)',
                    texname = '\\text{I101a14}')

I101a22 = Parameter(name = 'I101a22',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Rl2x4*complexconjugate(Rl2x4)',
                    texname = '\\text{I101a22}')

I101a33 = Parameter(name = 'I101a33',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Rl3x5*complexconjugate(Rl3x5)',
                    texname = '\\text{I101a33}')

I101a41 = Parameter(name = 'I101a41',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Rl1x6*complexconjugate(Rl4x6)',
                    texname = '\\text{I101a41}')

I101a44 = Parameter(name = 'I101a44',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Rl4x6*complexconjugate(Rl4x6)',
                    texname = '\\text{I101a44}')

I102a11 = Parameter(name = 'I102a11',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Ru1x6*complexconjugate(Ru1x6)',
                    texname = '\\text{I102a11}')

I102a12 = Parameter(name = 'I102a12',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Ru2x6*complexconjugate(Ru1x6)',
                    texname = '\\text{I102a12}')

I102a21 = Parameter(name = 'I102a21',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Ru1x6*complexconjugate(Ru2x6)',
                    texname = '\\text{I102a21}')

I102a22 = Parameter(name = 'I102a22',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Ru2x6*complexconjugate(Ru2x6)',
                    texname = '\\text{I102a22}')

I102a33 = Parameter(name = 'I102a33',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Ru3x5*complexconjugate(Ru3x5)',
                    texname = '\\text{I102a33}')

I102a44 = Parameter(name = 'I102a44',
                    nature = 'internal',
                    type = 'complex',
                    value = 'Ru4x4*complexconjugate(Ru4x4)',
                    texname = '\\text{I102a44}')

I11a23 = Parameter(name = 'I11a23',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd3x5*yd2x2',
                   texname = '\\text{I11a23}')

I11a31 = Parameter(name = 'I11a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x6*yd3x3',
                   texname = '\\text{I11a31}')

I11a32 = Parameter(name = 'I11a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x6*yd3x3',
                   texname = '\\text{I11a32}')

I12a11 = Parameter(name = 'I12a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I12a11}')

I12a12 = Parameter(name = 'I12a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I12a12}')

I12a21 = Parameter(name = 'I12a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I12a21}')

I12a22 = Parameter(name = 'I12a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I12a22}')

I12a55 = Parameter(name = 'I12a55',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd5x1*complexconjugate(Rd5x1)',
                   texname = '\\text{I12a55}')

I12a66 = Parameter(name = 'I12a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd6x2*complexconjugate(Rd6x2)',
                   texname = '\\text{I12a66}')

I13a11 = Parameter(name = 'I13a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x6*complexconjugate(Rd1x6)',
                   texname = '\\text{I13a11}')

I13a12 = Parameter(name = 'I13a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x6*complexconjugate(Rd1x6)',
                   texname = '\\text{I13a12}')

I13a21 = Parameter(name = 'I13a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x6*complexconjugate(Rd2x6)',
                   texname = '\\text{I13a21}')

I13a22 = Parameter(name = 'I13a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x6*complexconjugate(Rd2x6)',
                   texname = '\\text{I13a22}')

I13a33 = Parameter(name = 'I13a33',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd3x5*complexconjugate(Rd3x5)',
                   texname = '\\text{I13a33}')

I13a44 = Parameter(name = 'I13a44',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd4x4*complexconjugate(Rd4x4)',
                   texname = '\\text{I13a44}')

I14a22 = Parameter(name = 'I14a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(yd2x2)',
                   texname = '\\text{I14a22}')

I14a33 = Parameter(name = 'I14a33',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(yd3x3)',
                   texname = '\\text{I14a33}')

I15a22 = Parameter(name = 'I15a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'yu2x2',
                   texname = '\\text{I15a22}')

I15a33 = Parameter(name = 'I15a33',
                   nature = 'internal',
                   type = 'complex',
                   value = 'yu3x3',
                   texname = '\\text{I15a33}')

I16a11 = Parameter(name = 'I16a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(ye1x1)',
                   texname = '\\text{I16a11}')

I16a22 = Parameter(name = 'I16a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(ye2x2)',
                   texname = '\\text{I16a22}')

I16a33 = Parameter(name = 'I16a33',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(ye3x3)',
                   texname = '\\text{I16a33}')

I17a12 = Parameter(name = 'I17a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rl2x4)*complexconjugate(ye1x1)',
                   texname = '\\text{I17a12}')

I17a23 = Parameter(name = 'I17a23',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rl3x5)*complexconjugate(ye2x2)',
                   texname = '\\text{I17a23}')

I17a31 = Parameter(name = 'I17a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rl1x6)*complexconjugate(ye3x3)',
                   texname = '\\text{I17a31}')

I17a34 = Parameter(name = 'I17a34',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rl4x6)*complexconjugate(ye3x3)',
                   texname = '\\text{I17a34}')

I18a15 = Parameter(name = 'I18a15',
                   nature = 'internal',
                   type = 'complex',
                   value = 'ye1x1*complexconjugate(Rl5x1)',
                   texname = '\\text{I18a15}')

I18a26 = Parameter(name = 'I18a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'ye2x2*complexconjugate(Rl6x2)',
                   texname = '\\text{I18a26}')

I18a31 = Parameter(name = 'I18a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'ye3x3*complexconjugate(Rl1x3)',
                   texname = '\\text{I18a31}')

I18a34 = Parameter(name = 'I18a34',
                   nature = 'internal',
                   type = 'complex',
                   value = 'ye3x3*complexconjugate(Rl4x3)',
                   texname = '\\text{I18a34}')

I19a11 = Parameter(name = 'I19a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3*complexconjugate(Rl1x3)',
                   texname = '\\text{I19a11}')

I19a14 = Parameter(name = 'I19a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3*complexconjugate(Rl1x3)',
                   texname = '\\text{I19a14}')

I19a41 = Parameter(name = 'I19a41',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3*complexconjugate(Rl4x3)',
                   texname = '\\text{I19a41}')

I19a44 = Parameter(name = 'I19a44',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3*complexconjugate(Rl4x3)',
                   texname = '\\text{I19a44}')

I19a55 = Parameter(name = 'I19a55',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl5x1*complexconjugate(Rl5x1)',
                   texname = '\\text{I19a55}')

I19a66 = Parameter(name = 'I19a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl6x2*complexconjugate(Rl6x2)',
                   texname = '\\text{I19a66}')

I2a22 = Parameter(name = 'I2a22',
                  nature = 'internal',
                  type = 'complex',
                  value = 'yd2x2',
                  texname = '\\text{I2a22}')

I2a33 = Parameter(name = 'I2a33',
                  nature = 'internal',
                  type = 'complex',
                  value = 'yd3x3',
                  texname = '\\text{I2a33}')

I20a11 = Parameter(name = 'I20a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x6*complexconjugate(Rl1x6)',
                   texname = '\\text{I20a11}')

I20a14 = Parameter(name = 'I20a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x6*complexconjugate(Rl1x6)',
                   texname = '\\text{I20a14}')

I20a22 = Parameter(name = 'I20a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl2x4*complexconjugate(Rl2x4)',
                   texname = '\\text{I20a22}')

I20a33 = Parameter(name = 'I20a33',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl3x5*complexconjugate(Rl3x5)',
                   texname = '\\text{I20a33}')

I20a41 = Parameter(name = 'I20a41',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x6*complexconjugate(Rl4x6)',
                   texname = '\\text{I20a41}')

I20a44 = Parameter(name = 'I20a44',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x6*complexconjugate(Rl4x6)',
                   texname = '\\text{I20a44}')

I21a15 = Parameter(name = 'I21a15',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl5x1*complexconjugate(ye1x1)',
                   texname = '\\text{I21a15}')

I21a26 = Parameter(name = 'I21a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl6x2*complexconjugate(ye2x2)',
                   texname = '\\text{I21a26}')

I21a31 = Parameter(name = 'I21a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3*complexconjugate(ye3x3)',
                   texname = '\\text{I21a31}')

I21a34 = Parameter(name = 'I21a34',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3*complexconjugate(ye3x3)',
                   texname = '\\text{I21a34}')

I22a12 = Parameter(name = 'I22a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl2x4*ye1x1',
                   texname = '\\text{I22a12}')

I22a23 = Parameter(name = 'I22a23',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl3x5*ye2x2',
                   texname = '\\text{I22a23}')

I22a31 = Parameter(name = 'I22a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x6*ye3x3',
                   texname = '\\text{I22a31}')

I22a34 = Parameter(name = 'I22a34',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x6*ye3x3',
                   texname = '\\text{I22a34}')

I23a15 = Parameter(name = 'I23a15',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl5x1',
                   texname = '\\text{I23a15}')

I23a26 = Parameter(name = 'I23a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl6x2',
                   texname = '\\text{I23a26}')

I23a31 = Parameter(name = 'I23a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3',
                   texname = '\\text{I23a31}')

I23a34 = Parameter(name = 'I23a34',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3',
                   texname = '\\text{I23a34}')

I24a12 = Parameter(name = 'I24a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl2x4*ye1x1',
                   texname = '\\text{I24a12}')

I24a23 = Parameter(name = 'I24a23',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl3x5*ye2x2',
                   texname = '\\text{I24a23}')

I24a31 = Parameter(name = 'I24a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x6*ye3x3',
                   texname = '\\text{I24a31}')

I24a34 = Parameter(name = 'I24a34',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x6*ye3x3',
                   texname = '\\text{I24a34}')

I25a11 = Parameter(name = 'I25a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3*complexconjugate(Rl1x3)',
                   texname = '\\text{I25a11}')

I25a14 = Parameter(name = 'I25a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3*complexconjugate(Rl1x3)',
                   texname = '\\text{I25a14}')

I25a41 = Parameter(name = 'I25a41',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3*complexconjugate(Rl4x3)',
                   texname = '\\text{I25a41}')

I25a44 = Parameter(name = 'I25a44',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3*complexconjugate(Rl4x3)',
                   texname = '\\text{I25a44}')

I25a55 = Parameter(name = 'I25a55',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl5x1*complexconjugate(Rl5x1)',
                   texname = '\\text{I25a55}')

I25a66 = Parameter(name = 'I25a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl6x2*complexconjugate(Rl6x2)',
                   texname = '\\text{I25a66}')

I26a11 = Parameter(name = 'I26a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x6*complexconjugate(Rl1x6)',
                   texname = '\\text{I26a11}')

I26a14 = Parameter(name = 'I26a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x6*complexconjugate(Rl1x6)',
                   texname = '\\text{I26a14}')

I26a22 = Parameter(name = 'I26a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl2x4*complexconjugate(Rl2x4)',
                   texname = '\\text{I26a22}')

I26a33 = Parameter(name = 'I26a33',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl3x5*complexconjugate(Rl3x5)',
                   texname = '\\text{I26a33}')

I26a41 = Parameter(name = 'I26a41',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x6*complexconjugate(Rl4x6)',
                   texname = '\\text{I26a41}')

I26a44 = Parameter(name = 'I26a44',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x6*complexconjugate(Rl4x6)',
                   texname = '\\text{I26a44}')

I27a11 = Parameter(name = 'I27a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3*complexconjugate(Rn1x3)',
                   texname = '\\text{I27a11}')

I27a14 = Parameter(name = 'I27a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3*complexconjugate(Rn1x3)',
                   texname = '\\text{I27a14}')

I27a26 = Parameter(name = 'I27a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl6x2*complexconjugate(Rn2x2)',
                   texname = '\\text{I27a26}')

I27a35 = Parameter(name = 'I27a35',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl5x1*complexconjugate(Rn3x1)',
                   texname = '\\text{I27a35}')

I28a11 = Parameter(name = 'I28a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x6*te3x3*complexconjugate(Rn1x3)',
                   texname = '\\text{I28a11}')

I28a14 = Parameter(name = 'I28a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x6*te3x3*complexconjugate(Rn1x3)',
                   texname = '\\text{I28a14}')

I29a11 = Parameter(name = 'I29a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3*ye3x3*complexconjugate(Rn1x3)*complexconjugate(ye3x3)',
                   texname = '\\text{I29a11}')

I29a14 = Parameter(name = 'I29a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3*ye3x3*complexconjugate(Rn1x3)*complexconjugate(ye3x3)',
                   texname = '\\text{I29a14}')

I29a26 = Parameter(name = 'I29a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl6x2*ye2x2*complexconjugate(Rn2x2)*complexconjugate(ye2x2)',
                   texname = '\\text{I29a26}')

I29a35 = Parameter(name = 'I29a35',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl5x1*ye1x1*complexconjugate(Rn3x1)*complexconjugate(ye1x1)',
                   texname = '\\text{I29a35}')

I3a23 = Parameter(name = 'I3a23',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complexconjugate(Rd3x5)*complexconjugate(yd2x2)',
                  texname = '\\text{I3a23}')

I3a31 = Parameter(name = 'I3a31',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complexconjugate(Rd1x6)*complexconjugate(yd3x3)',
                  texname = '\\text{I3a31}')

I3a32 = Parameter(name = 'I3a32',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complexconjugate(Rd2x6)*complexconjugate(yd3x3)',
                  texname = '\\text{I3a32}')

I30a11 = Parameter(name = 'I30a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x6*ye3x3*complexconjugate(Rn1x3)',
                   texname = '\\text{I30a11}')

I30a14 = Parameter(name = 'I30a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x6*ye3x3*complexconjugate(Rn1x3)',
                   texname = '\\text{I30a14}')

I30a23 = Parameter(name = 'I30a23',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl3x5*ye2x2*complexconjugate(Rn2x2)',
                   texname = '\\text{I30a23}')

I30a32 = Parameter(name = 'I30a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl2x4*ye1x1*complexconjugate(Rn3x1)',
                   texname = '\\text{I30a32}')

I31a13 = Parameter(name = 'I31a13',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn3x1',
                   texname = '\\text{I31a13}')

I31a22 = Parameter(name = 'I31a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn2x2',
                   texname = '\\text{I31a22}')

I31a31 = Parameter(name = 'I31a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn1x3',
                   texname = '\\text{I31a31}')

I32a13 = Parameter(name = 'I32a13',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn3x1*complexconjugate(ye1x1)',
                   texname = '\\text{I32a13}')

I32a22 = Parameter(name = 'I32a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn2x2*complexconjugate(ye2x2)',
                   texname = '\\text{I32a22}')

I32a31 = Parameter(name = 'I32a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn1x3*complexconjugate(ye3x3)',
                   texname = '\\text{I32a31}')

I33a11 = Parameter(name = 'I33a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn1x3*complexconjugate(Rl1x3)',
                   texname = '\\text{I33a11}')

I33a14 = Parameter(name = 'I33a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn1x3*complexconjugate(Rl4x3)',
                   texname = '\\text{I33a14}')

I33a26 = Parameter(name = 'I33a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn2x2*complexconjugate(Rl6x2)',
                   texname = '\\text{I33a26}')

I33a35 = Parameter(name = 'I33a35',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn3x1*complexconjugate(Rl5x1)',
                   texname = '\\text{I33a35}')

I34a11 = Parameter(name = 'I34a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn1x3*complexconjugate(Rl1x6)*complexconjugate(ye3x3)',
                   texname = '\\text{I34a11}')

I34a14 = Parameter(name = 'I34a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn1x3*complexconjugate(Rl4x6)*complexconjugate(ye3x3)',
                   texname = '\\text{I34a14}')

I34a23 = Parameter(name = 'I34a23',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn2x2*complexconjugate(Rl3x5)*complexconjugate(ye2x2)',
                   texname = '\\text{I34a23}')

I34a32 = Parameter(name = 'I34a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn3x1*complexconjugate(Rl2x4)*complexconjugate(ye1x1)',
                   texname = '\\text{I34a32}')

I35a11 = Parameter(name = 'I35a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn1x3*complexconjugate(Rl1x6)*complexconjugate(te3x3)',
                   texname = '\\text{I35a11}')

I35a14 = Parameter(name = 'I35a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn1x3*complexconjugate(Rl4x6)*complexconjugate(te3x3)',
                   texname = '\\text{I35a14}')

I36a11 = Parameter(name = 'I36a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn1x3*ye3x3*complexconjugate(Rl1x3)*complexconjugate(ye3x3)',
                   texname = '\\text{I36a11}')

I36a14 = Parameter(name = 'I36a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn1x3*ye3x3*complexconjugate(Rl4x3)*complexconjugate(ye3x3)',
                   texname = '\\text{I36a14}')

I36a26 = Parameter(name = 'I36a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn2x2*ye2x2*complexconjugate(Rl6x2)*complexconjugate(ye2x2)',
                   texname = '\\text{I36a26}')

I36a35 = Parameter(name = 'I36a35',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn3x1*ye1x1*complexconjugate(Rl5x1)*complexconjugate(ye1x1)',
                   texname = '\\text{I36a35}')

I37a23 = Parameter(name = 'I37a23',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Ru3x5)*complexconjugate(yu2x2)',
                   texname = '\\text{I37a23}')

I37a31 = Parameter(name = 'I37a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Ru1x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I37a31}')

I37a32 = Parameter(name = 'I37a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Ru2x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I37a32}')

I38a26 = Parameter(name = 'I38a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'yu2x2*complexconjugate(Ru6x2)',
                   texname = '\\text{I38a26}')

I38a31 = Parameter(name = 'I38a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'yu3x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I38a31}')

I38a32 = Parameter(name = 'I38a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'yu3x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I38a32}')

I39a11 = Parameter(name = 'I39a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I39a11}')

I39a12 = Parameter(name = 'I39a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I39a12}')

I39a21 = Parameter(name = 'I39a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I39a21}')

I39a22 = Parameter(name = 'I39a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I39a22}')

I39a55 = Parameter(name = 'I39a55',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru5x1*complexconjugate(Ru5x1)',
                   texname = '\\text{I39a55}')

I39a66 = Parameter(name = 'I39a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru6x2*complexconjugate(Ru6x2)',
                   texname = '\\text{I39a66}')

I4a26 = Parameter(name = 'I4a26',
                  nature = 'internal',
                  type = 'complex',
                  value = 'yd2x2*complexconjugate(Rd6x2)',
                  texname = '\\text{I4a26}')

I4a31 = Parameter(name = 'I4a31',
                  nature = 'internal',
                  type = 'complex',
                  value = 'yd3x3*complexconjugate(Rd1x3)',
                  texname = '\\text{I4a31}')

I4a32 = Parameter(name = 'I4a32',
                  nature = 'internal',
                  type = 'complex',
                  value = 'yd3x3*complexconjugate(Rd2x3)',
                  texname = '\\text{I4a32}')

I40a11 = Parameter(name = 'I40a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*complexconjugate(Ru1x6)',
                   texname = '\\text{I40a11}')

I40a12 = Parameter(name = 'I40a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*complexconjugate(Ru1x6)',
                   texname = '\\text{I40a12}')

I40a21 = Parameter(name = 'I40a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*complexconjugate(Ru2x6)',
                   texname = '\\text{I40a21}')

I40a22 = Parameter(name = 'I40a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*complexconjugate(Ru2x6)',
                   texname = '\\text{I40a22}')

I40a33 = Parameter(name = 'I40a33',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru3x5*complexconjugate(Ru3x5)',
                   texname = '\\text{I40a33}')

I40a44 = Parameter(name = 'I40a44',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru4x4*complexconjugate(Ru4x4)',
                   texname = '\\text{I40a44}')

I41a11 = Parameter(name = 'I41a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I41a11}')

I41a12 = Parameter(name = 'I41a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I41a12}')

I41a21 = Parameter(name = 'I41a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I41a21}')

I41a22 = Parameter(name = 'I41a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I41a22}')

I41a55 = Parameter(name = 'I41a55',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd5x1*complexconjugate(Ru5x1)',
                   texname = '\\text{I41a55}')

I41a66 = Parameter(name = 'I41a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd6x2*complexconjugate(Ru6x2)',
                   texname = '\\text{I41a66}')

I42a11 = Parameter(name = 'I42a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(Ru1x6)*complexconjugate(tu3x3)',
                   texname = '\\text{I42a11}')

I42a12 = Parameter(name = 'I42a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(Ru2x6)*complexconjugate(tu3x3)',
                   texname = '\\text{I42a12}')

I42a21 = Parameter(name = 'I42a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(Ru1x6)*complexconjugate(tu3x3)',
                   texname = '\\text{I42a21}')

I42a22 = Parameter(name = 'I42a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(Ru2x6)*complexconjugate(tu3x3)',
                   texname = '\\text{I42a22}')

I43a11 = Parameter(name = 'I43a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(Ru1x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I43a11}')

I43a12 = Parameter(name = 'I43a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(Ru2x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I43a12}')

I43a21 = Parameter(name = 'I43a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(Ru1x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I43a21}')

I43a22 = Parameter(name = 'I43a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(Ru2x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I43a22}')

I43a63 = Parameter(name = 'I43a63',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd6x2*complexconjugate(Ru3x5)*complexconjugate(yu2x2)',
                   texname = '\\text{I43a63}')

I44a11 = Parameter(name = 'I44a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x6*td3x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I44a11}')

I44a12 = Parameter(name = 'I44a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x6*td3x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I44a12}')

I44a21 = Parameter(name = 'I44a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x6*td3x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I44a21}')

I44a22 = Parameter(name = 'I44a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x6*td3x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I44a22}')

I45a11 = Parameter(name = 'I45a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x6*yd3x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I45a11}')

I45a12 = Parameter(name = 'I45a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x6*yd3x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I45a12}')

I45a21 = Parameter(name = 'I45a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x6*yd3x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I45a21}')

I45a22 = Parameter(name = 'I45a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x6*yd3x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I45a22}')

I45a36 = Parameter(name = 'I45a36',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd3x5*yd2x2*complexconjugate(Ru6x2)',
                   texname = '\\text{I45a36}')

I46a11 = Parameter(name = 'I46a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*yd3x3*complexconjugate(Ru1x3)*complexconjugate(yd3x3)',
                   texname = '\\text{I46a11}')

I46a12 = Parameter(name = 'I46a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*yd3x3*complexconjugate(Ru2x3)*complexconjugate(yd3x3)',
                   texname = '\\text{I46a12}')

I46a21 = Parameter(name = 'I46a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*yd3x3*complexconjugate(Ru1x3)*complexconjugate(yd3x3)',
                   texname = '\\text{I46a21}')

I46a22 = Parameter(name = 'I46a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*yd3x3*complexconjugate(Ru2x3)*complexconjugate(yd3x3)',
                   texname = '\\text{I46a22}')

I46a66 = Parameter(name = 'I46a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd6x2*yd2x2*complexconjugate(Ru6x2)*complexconjugate(yd2x2)',
                   texname = '\\text{I46a66}')

I47a11 = Parameter(name = 'I47a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x6*yd3x3*complexconjugate(Ru1x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I47a11}')

I47a12 = Parameter(name = 'I47a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x6*yd3x3*complexconjugate(Ru2x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I47a12}')

I47a21 = Parameter(name = 'I47a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x6*yd3x3*complexconjugate(Ru1x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I47a21}')

I47a22 = Parameter(name = 'I47a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x6*yd3x3*complexconjugate(Ru2x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I47a22}')

I47a33 = Parameter(name = 'I47a33',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd3x5*yd2x2*complexconjugate(Ru3x5)*complexconjugate(yu2x2)',
                   texname = '\\text{I47a33}')

I48a11 = Parameter(name = 'I48a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*yu3x3*complexconjugate(Ru1x3)*complexconjugate(yu3x3)',
                   texname = '\\text{I48a11}')

I48a12 = Parameter(name = 'I48a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*yu3x3*complexconjugate(Ru2x3)*complexconjugate(yu3x3)',
                   texname = '\\text{I48a12}')

I48a21 = Parameter(name = 'I48a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*yu3x3*complexconjugate(Ru1x3)*complexconjugate(yu3x3)',
                   texname = '\\text{I48a21}')

I48a22 = Parameter(name = 'I48a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*yu3x3*complexconjugate(Ru2x3)*complexconjugate(yu3x3)',
                   texname = '\\text{I48a22}')

I48a66 = Parameter(name = 'I48a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd6x2*yu2x2*complexconjugate(Ru6x2)*complexconjugate(yu2x2)',
                   texname = '\\text{I48a66}')

I49a26 = Parameter(name = 'I49a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru6x2*complexconjugate(yu2x2)',
                   texname = '\\text{I49a26}')

I49a31 = Parameter(name = 'I49a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(yu3x3)',
                   texname = '\\text{I49a31}')

I49a32 = Parameter(name = 'I49a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(yu3x3)',
                   texname = '\\text{I49a32}')

I5a11 = Parameter(name = 'I5a11',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd1x3*complexconjugate(Rd1x3)',
                  texname = '\\text{I5a11}')

I5a12 = Parameter(name = 'I5a12',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd2x3*complexconjugate(Rd1x3)',
                  texname = '\\text{I5a12}')

I5a21 = Parameter(name = 'I5a21',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd1x3*complexconjugate(Rd2x3)',
                  texname = '\\text{I5a21}')

I5a22 = Parameter(name = 'I5a22',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd2x3*complexconjugate(Rd2x3)',
                  texname = '\\text{I5a22}')

I5a55 = Parameter(name = 'I5a55',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd5x1*complexconjugate(Rd5x1)',
                  texname = '\\text{I5a55}')

I5a66 = Parameter(name = 'I5a66',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd6x2*complexconjugate(Rd6x2)',
                  texname = '\\text{I5a66}')

I50a23 = Parameter(name = 'I50a23',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru3x5*yu2x2',
                   texname = '\\text{I50a23}')

I50a31 = Parameter(name = 'I50a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*yu3x3',
                   texname = '\\text{I50a31}')

I50a32 = Parameter(name = 'I50a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*yu3x3',
                   texname = '\\text{I50a32}')

I51a15 = Parameter(name = 'I51a15',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru5x1',
                   texname = '\\text{I51a15}')

I51a26 = Parameter(name = 'I51a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru6x2',
                   texname = '\\text{I51a26}')

I51a31 = Parameter(name = 'I51a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3',
                   texname = '\\text{I51a31}')

I51a32 = Parameter(name = 'I51a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3',
                   texname = '\\text{I51a32}')

I52a26 = Parameter(name = 'I52a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru6x2*complexconjugate(yd2x2)',
                   texname = '\\text{I52a26}')

I52a31 = Parameter(name = 'I52a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(yd3x3)',
                   texname = '\\text{I52a31}')

I52a32 = Parameter(name = 'I52a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(yd3x3)',
                   texname = '\\text{I52a32}')

I53a23 = Parameter(name = 'I53a23',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru3x5*yu2x2',
                   texname = '\\text{I53a23}')

I53a31 = Parameter(name = 'I53a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*yu3x3',
                   texname = '\\text{I53a31}')

I53a32 = Parameter(name = 'I53a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*yu3x3',
                   texname = '\\text{I53a32}')

I54a11 = Parameter(name = 'I54a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I54a11}')

I54a12 = Parameter(name = 'I54a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I54a12}')

I54a21 = Parameter(name = 'I54a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I54a21}')

I54a22 = Parameter(name = 'I54a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I54a22}')

I54a55 = Parameter(name = 'I54a55',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru5x1*complexconjugate(Rd5x1)',
                   texname = '\\text{I54a55}')

I54a66 = Parameter(name = 'I54a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru6x2*complexconjugate(Rd6x2)',
                   texname = '\\text{I54a66}')

I55a11 = Parameter(name = 'I55a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Rd1x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I55a11}')

I55a12 = Parameter(name = 'I55a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Rd1x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I55a12}')

I55a21 = Parameter(name = 'I55a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Rd2x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I55a21}')

I55a22 = Parameter(name = 'I55a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Rd2x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I55a22}')

I55a36 = Parameter(name = 'I55a36',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru6x2*complexconjugate(Rd3x5)*complexconjugate(yd2x2)',
                   texname = '\\text{I55a36}')

I56a11 = Parameter(name = 'I56a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Rd1x6)*complexconjugate(td3x3)',
                   texname = '\\text{I56a11}')

I56a12 = Parameter(name = 'I56a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Rd1x6)*complexconjugate(td3x3)',
                   texname = '\\text{I56a12}')

I56a21 = Parameter(name = 'I56a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Rd2x6)*complexconjugate(td3x3)',
                   texname = '\\text{I56a21}')

I56a22 = Parameter(name = 'I56a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Rd2x6)*complexconjugate(td3x3)',
                   texname = '\\text{I56a22}')

I57a11 = Parameter(name = 'I57a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*tu3x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I57a11}')

I57a12 = Parameter(name = 'I57a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*tu3x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I57a12}')

I57a21 = Parameter(name = 'I57a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*tu3x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I57a21}')

I57a22 = Parameter(name = 'I57a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*tu3x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I57a22}')

I58a11 = Parameter(name = 'I58a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*yd3x3*complexconjugate(Rd1x3)*complexconjugate(yd3x3)',
                   texname = '\\text{I58a11}')

I58a12 = Parameter(name = 'I58a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*yd3x3*complexconjugate(Rd1x3)*complexconjugate(yd3x3)',
                   texname = '\\text{I58a12}')

I58a21 = Parameter(name = 'I58a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*yd3x3*complexconjugate(Rd2x3)*complexconjugate(yd3x3)',
                   texname = '\\text{I58a21}')

I58a22 = Parameter(name = 'I58a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*yd3x3*complexconjugate(Rd2x3)*complexconjugate(yd3x3)',
                   texname = '\\text{I58a22}')

I58a66 = Parameter(name = 'I58a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru6x2*yd2x2*complexconjugate(Rd6x2)*complexconjugate(yd2x2)',
                   texname = '\\text{I58a66}')

I59a11 = Parameter(name = 'I59a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*yu3x3*complexconjugate(Rd1x3)*complexconjugate(yu3x3)',
                   texname = '\\text{I59a11}')

I59a12 = Parameter(name = 'I59a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*yu3x3*complexconjugate(Rd1x3)*complexconjugate(yu3x3)',
                   texname = '\\text{I59a12}')

I59a21 = Parameter(name = 'I59a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*yu3x3*complexconjugate(Rd2x3)*complexconjugate(yu3x3)',
                   texname = '\\text{I59a21}')

I59a22 = Parameter(name = 'I59a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*yu3x3*complexconjugate(Rd2x3)*complexconjugate(yu3x3)',
                   texname = '\\text{I59a22}')

I59a66 = Parameter(name = 'I59a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru6x2*yu2x2*complexconjugate(Rd6x2)*complexconjugate(yu2x2)',
                   texname = '\\text{I59a66}')

I6a11 = Parameter(name = 'I6a11',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd1x6*complexconjugate(Rd1x6)',
                  texname = '\\text{I6a11}')

I6a12 = Parameter(name = 'I6a12',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd2x6*complexconjugate(Rd1x6)',
                  texname = '\\text{I6a12}')

I6a21 = Parameter(name = 'I6a21',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd1x6*complexconjugate(Rd2x6)',
                  texname = '\\text{I6a21}')

I6a22 = Parameter(name = 'I6a22',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd2x6*complexconjugate(Rd2x6)',
                  texname = '\\text{I6a22}')

I6a33 = Parameter(name = 'I6a33',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd3x5*complexconjugate(Rd3x5)',
                  texname = '\\text{I6a33}')

I6a44 = Parameter(name = 'I6a44',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd4x4*complexconjugate(Rd4x4)',
                  texname = '\\text{I6a44}')

I60a11 = Parameter(name = 'I60a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*yu3x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I60a11}')

I60a12 = Parameter(name = 'I60a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*yu3x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I60a12}')

I60a21 = Parameter(name = 'I60a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*yu3x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I60a21}')

I60a22 = Parameter(name = 'I60a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*yu3x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I60a22}')

I60a63 = Parameter(name = 'I60a63',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru3x5*yu2x2*complexconjugate(Rd6x2)',
                   texname = '\\text{I60a63}')

I61a11 = Parameter(name = 'I61a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*yu3x3*complexconjugate(Rd1x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I61a11}')

I61a12 = Parameter(name = 'I61a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*yu3x3*complexconjugate(Rd1x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I61a12}')

I61a21 = Parameter(name = 'I61a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*yu3x3*complexconjugate(Rd2x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I61a21}')

I61a22 = Parameter(name = 'I61a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*yu3x3*complexconjugate(Rd2x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I61a22}')

I61a33 = Parameter(name = 'I61a33',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru3x5*yu2x2*complexconjugate(Rd3x5)*complexconjugate(yd2x2)',
                   texname = '\\text{I61a33}')

I62a11 = Parameter(name = 'I62a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I62a11}')

I62a12 = Parameter(name = 'I62a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I62a12}')

I62a21 = Parameter(name = 'I62a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I62a21}')

I62a22 = Parameter(name = 'I62a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I62a22}')

I62a55 = Parameter(name = 'I62a55',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru5x1*complexconjugate(Ru5x1)',
                   texname = '\\text{I62a55}')

I62a66 = Parameter(name = 'I62a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru6x2*complexconjugate(Ru6x2)',
                   texname = '\\text{I62a66}')

I63a11 = Parameter(name = 'I63a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*complexconjugate(Ru1x6)',
                   texname = '\\text{I63a11}')

I63a12 = Parameter(name = 'I63a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*complexconjugate(Ru1x6)',
                   texname = '\\text{I63a12}')

I63a21 = Parameter(name = 'I63a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*complexconjugate(Ru2x6)',
                   texname = '\\text{I63a21}')

I63a22 = Parameter(name = 'I63a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*complexconjugate(Ru2x6)',
                   texname = '\\text{I63a22}')

I63a33 = Parameter(name = 'I63a33',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru3x5*complexconjugate(Ru3x5)',
                   texname = '\\text{I63a33}')

I63a44 = Parameter(name = 'I63a44',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru4x4*complexconjugate(Ru4x4)',
                   texname = '\\text{I63a44}')

I64a11 = Parameter(name = 'I64a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(Rd1x6)*complexconjugate(td3x3)',
                   texname = '\\text{I64a11}')

I64a12 = Parameter(name = 'I64a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(Rd1x6)*complexconjugate(td3x3)',
                   texname = '\\text{I64a12}')

I64a21 = Parameter(name = 'I64a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(Rd2x6)*complexconjugate(td3x3)',
                   texname = '\\text{I64a21}')

I64a22 = Parameter(name = 'I64a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(Rd2x6)*complexconjugate(td3x3)',
                   texname = '\\text{I64a22}')

I65a11 = Parameter(name = 'I65a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x6*td3x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I65a11}')

I65a12 = Parameter(name = 'I65a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x6*td3x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I65a12}')

I65a21 = Parameter(name = 'I65a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x6*td3x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I65a21}')

I65a22 = Parameter(name = 'I65a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x6*td3x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I65a22}')

I66a11 = Parameter(name = 'I66a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(Rd1x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I66a11}')

I66a12 = Parameter(name = 'I66a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(Rd1x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I66a12}')

I66a21 = Parameter(name = 'I66a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(Rd2x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I66a21}')

I66a22 = Parameter(name = 'I66a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(Rd2x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I66a22}')

I66a36 = Parameter(name = 'I66a36',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd6x2*complexconjugate(Rd3x5)*complexconjugate(yd2x2)',
                   texname = '\\text{I66a36}')

I67a11 = Parameter(name = 'I67a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x6*yd3x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I67a11}')

I67a12 = Parameter(name = 'I67a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x6*yd3x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I67a12}')

I67a21 = Parameter(name = 'I67a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x6*yd3x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I67a21}')

I67a22 = Parameter(name = 'I67a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x6*yd3x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I67a22}')

I67a63 = Parameter(name = 'I67a63',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd3x5*yd2x2*complexconjugate(Rd6x2)',
                   texname = '\\text{I67a63}')

I68a11 = Parameter(name = 'I68a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3*complexconjugate(Rl1x6)*complexconjugate(te3x3)',
                   texname = '\\text{I68a11}')

I68a14 = Parameter(name = 'I68a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3*complexconjugate(Rl1x6)*complexconjugate(te3x3)',
                   texname = '\\text{I68a14}')

I68a41 = Parameter(name = 'I68a41',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3*complexconjugate(Rl4x6)*complexconjugate(te3x3)',
                   texname = '\\text{I68a41}')

I68a44 = Parameter(name = 'I68a44',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3*complexconjugate(Rl4x6)*complexconjugate(te3x3)',
                   texname = '\\text{I68a44}')

I69a11 = Parameter(name = 'I69a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x6*te3x3*complexconjugate(Rl1x3)',
                   texname = '\\text{I69a11}')

I69a14 = Parameter(name = 'I69a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x6*te3x3*complexconjugate(Rl1x3)',
                   texname = '\\text{I69a14}')

I69a41 = Parameter(name = 'I69a41',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x6*te3x3*complexconjugate(Rl4x3)',
                   texname = '\\text{I69a41}')

I69a44 = Parameter(name = 'I69a44',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x6*te3x3*complexconjugate(Rl4x3)',
                   texname = '\\text{I69a44}')

I7a26 = Parameter(name = 'I7a26',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd6x2*complexconjugate(yd2x2)',
                  texname = '\\text{I7a26}')

I7a31 = Parameter(name = 'I7a31',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd1x3*complexconjugate(yd3x3)',
                  texname = '\\text{I7a31}')

I7a32 = Parameter(name = 'I7a32',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd2x3*complexconjugate(yd3x3)',
                  texname = '\\text{I7a32}')

I70a11 = Parameter(name = 'I70a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3*complexconjugate(Rl1x6)*complexconjugate(ye3x3)',
                   texname = '\\text{I70a11}')

I70a14 = Parameter(name = 'I70a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3*complexconjugate(Rl1x6)*complexconjugate(ye3x3)',
                   texname = '\\text{I70a14}')

I70a25 = Parameter(name = 'I70a25',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl5x1*complexconjugate(Rl2x4)*complexconjugate(ye1x1)',
                   texname = '\\text{I70a25}')

I70a36 = Parameter(name = 'I70a36',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl6x2*complexconjugate(Rl3x5)*complexconjugate(ye2x2)',
                   texname = '\\text{I70a36}')

I70a41 = Parameter(name = 'I70a41',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3*complexconjugate(Rl4x6)*complexconjugate(ye3x3)',
                   texname = '\\text{I70a41}')

I70a44 = Parameter(name = 'I70a44',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3*complexconjugate(Rl4x6)*complexconjugate(ye3x3)',
                   texname = '\\text{I70a44}')

I71a11 = Parameter(name = 'I71a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x6*ye3x3*complexconjugate(Rl1x3)',
                   texname = '\\text{I71a11}')

I71a14 = Parameter(name = 'I71a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x6*ye3x3*complexconjugate(Rl1x3)',
                   texname = '\\text{I71a14}')

I71a41 = Parameter(name = 'I71a41',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x6*ye3x3*complexconjugate(Rl4x3)',
                   texname = '\\text{I71a41}')

I71a44 = Parameter(name = 'I71a44',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x6*ye3x3*complexconjugate(Rl4x3)',
                   texname = '\\text{I71a44}')

I71a52 = Parameter(name = 'I71a52',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl2x4*ye1x1*complexconjugate(Rl5x1)',
                   texname = '\\text{I71a52}')

I71a63 = Parameter(name = 'I71a63',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl3x5*ye2x2*complexconjugate(Rl6x2)',
                   texname = '\\text{I71a63}')

I72a11 = Parameter(name = 'I72a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Ru1x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I72a11}')

I72a12 = Parameter(name = 'I72a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Ru1x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I72a12}')

I72a21 = Parameter(name = 'I72a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Ru2x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I72a21}')

I72a22 = Parameter(name = 'I72a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Ru2x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I72a22}')

I72a36 = Parameter(name = 'I72a36',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru6x2*complexconjugate(Ru3x5)*complexconjugate(yu2x2)',
                   texname = '\\text{I72a36}')

I73a11 = Parameter(name = 'I73a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Ru1x6)*complexconjugate(tu3x3)',
                   texname = '\\text{I73a11}')

I73a12 = Parameter(name = 'I73a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Ru1x6)*complexconjugate(tu3x3)',
                   texname = '\\text{I73a12}')

I73a21 = Parameter(name = 'I73a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Ru2x6)*complexconjugate(tu3x3)',
                   texname = '\\text{I73a21}')

I73a22 = Parameter(name = 'I73a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Ru2x6)*complexconjugate(tu3x3)',
                   texname = '\\text{I73a22}')

I74a11 = Parameter(name = 'I74a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*tu3x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I74a11}')

I74a12 = Parameter(name = 'I74a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*tu3x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I74a12}')

I74a21 = Parameter(name = 'I74a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*tu3x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I74a21}')

I74a22 = Parameter(name = 'I74a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*tu3x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I74a22}')

I75a11 = Parameter(name = 'I75a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*yu3x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I75a11}')

I75a12 = Parameter(name = 'I75a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*yu3x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I75a12}')

I75a21 = Parameter(name = 'I75a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*yu3x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I75a21}')

I75a22 = Parameter(name = 'I75a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*yu3x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I75a22}')

I75a63 = Parameter(name = 'I75a63',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru3x5*yu2x2*complexconjugate(Ru6x2)',
                   texname = '\\text{I75a63}')

I76a11 = Parameter(name = 'I76a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*yd3x3*complexconjugate(Rd1x3)*complexconjugate(yd3x3)',
                   texname = '\\text{I76a11}')

I76a12 = Parameter(name = 'I76a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*yd3x3*complexconjugate(Rd1x3)*complexconjugate(yd3x3)',
                   texname = '\\text{I76a12}')

I76a21 = Parameter(name = 'I76a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*yd3x3*complexconjugate(Rd2x3)*complexconjugate(yd3x3)',
                   texname = '\\text{I76a21}')

I76a22 = Parameter(name = 'I76a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*yd3x3*complexconjugate(Rd2x3)*complexconjugate(yd3x3)',
                   texname = '\\text{I76a22}')

I76a66 = Parameter(name = 'I76a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd6x2*yd2x2*complexconjugate(Rd6x2)*complexconjugate(yd2x2)',
                   texname = '\\text{I76a66}')

I77a11 = Parameter(name = 'I77a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x6*yd3x3*complexconjugate(Rd1x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I77a11}')

I77a12 = Parameter(name = 'I77a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x6*yd3x3*complexconjugate(Rd1x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I77a12}')

I77a21 = Parameter(name = 'I77a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x6*yd3x3*complexconjugate(Rd2x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I77a21}')

I77a22 = Parameter(name = 'I77a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x6*yd3x3*complexconjugate(Rd2x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I77a22}')

I77a33 = Parameter(name = 'I77a33',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd3x5*yd2x2*complexconjugate(Rd3x5)*complexconjugate(yd2x2)',
                   texname = '\\text{I77a33}')

I78a11 = Parameter(name = 'I78a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3*ye3x3*complexconjugate(Rl1x3)*complexconjugate(ye3x3)',
                   texname = '\\text{I78a11}')

I78a14 = Parameter(name = 'I78a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3*ye3x3*complexconjugate(Rl1x3)*complexconjugate(ye3x3)',
                   texname = '\\text{I78a14}')

I78a41 = Parameter(name = 'I78a41',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3*ye3x3*complexconjugate(Rl4x3)*complexconjugate(ye3x3)',
                   texname = '\\text{I78a41}')

I78a44 = Parameter(name = 'I78a44',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3*ye3x3*complexconjugate(Rl4x3)*complexconjugate(ye3x3)',
                   texname = '\\text{I78a44}')

I78a55 = Parameter(name = 'I78a55',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl5x1*ye1x1*complexconjugate(Rl5x1)*complexconjugate(ye1x1)',
                   texname = '\\text{I78a55}')

I78a66 = Parameter(name = 'I78a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl6x2*ye2x2*complexconjugate(Rl6x2)*complexconjugate(ye2x2)',
                   texname = '\\text{I78a66}')

I79a11 = Parameter(name = 'I79a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x6*ye3x3*complexconjugate(Rl1x6)*complexconjugate(ye3x3)',
                   texname = '\\text{I79a11}')

I79a14 = Parameter(name = 'I79a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x6*ye3x3*complexconjugate(Rl1x6)*complexconjugate(ye3x3)',
                   texname = '\\text{I79a14}')

I79a22 = Parameter(name = 'I79a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl2x4*ye1x1*complexconjugate(Rl2x4)*complexconjugate(ye1x1)',
                   texname = '\\text{I79a22}')

I79a33 = Parameter(name = 'I79a33',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl3x5*ye2x2*complexconjugate(Rl3x5)*complexconjugate(ye2x2)',
                   texname = '\\text{I79a33}')

I79a41 = Parameter(name = 'I79a41',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x6*ye3x3*complexconjugate(Rl4x6)*complexconjugate(ye3x3)',
                   texname = '\\text{I79a41}')

I79a44 = Parameter(name = 'I79a44',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x6*ye3x3*complexconjugate(Rl4x6)*complexconjugate(ye3x3)',
                   texname = '\\text{I79a44}')

I8a23 = Parameter(name = 'I8a23',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd3x5*yd2x2',
                  texname = '\\text{I8a23}')

I8a31 = Parameter(name = 'I8a31',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd1x6*yd3x3',
                  texname = '\\text{I8a31}')

I8a32 = Parameter(name = 'I8a32',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd2x6*yd3x3',
                  texname = '\\text{I8a32}')

I80a11 = Parameter(name = 'I80a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*yu3x3*complexconjugate(Ru1x3)*complexconjugate(yu3x3)',
                   texname = '\\text{I80a11}')

I80a12 = Parameter(name = 'I80a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*yu3x3*complexconjugate(Ru1x3)*complexconjugate(yu3x3)',
                   texname = '\\text{I80a12}')

I80a21 = Parameter(name = 'I80a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*yu3x3*complexconjugate(Ru2x3)*complexconjugate(yu3x3)',
                   texname = '\\text{I80a21}')

I80a22 = Parameter(name = 'I80a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*yu3x3*complexconjugate(Ru2x3)*complexconjugate(yu3x3)',
                   texname = '\\text{I80a22}')

I80a66 = Parameter(name = 'I80a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru6x2*yu2x2*complexconjugate(Ru6x2)*complexconjugate(yu2x2)',
                   texname = '\\text{I80a66}')

I81a11 = Parameter(name = 'I81a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*yu3x3*complexconjugate(Ru1x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I81a11}')

I81a12 = Parameter(name = 'I81a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*yu3x3*complexconjugate(Ru1x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I81a12}')

I81a21 = Parameter(name = 'I81a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x6*yu3x3*complexconjugate(Ru2x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I81a21}')

I81a22 = Parameter(name = 'I81a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x6*yu3x3*complexconjugate(Ru2x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I81a22}')

I81a33 = Parameter(name = 'I81a33',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru3x5*yu2x2*complexconjugate(Ru3x5)*complexconjugate(yu2x2)',
                   texname = '\\text{I81a33}')

I82a15 = Parameter(name = 'I82a15',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rd5x1)',
                   texname = '\\text{I82a15}')

I82a26 = Parameter(name = 'I82a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rd6x2)',
                   texname = '\\text{I82a26}')

I82a31 = Parameter(name = 'I82a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rd1x3)',
                   texname = '\\text{I82a31}')

I82a32 = Parameter(name = 'I82a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rd2x3)',
                   texname = '\\text{I82a32}')

I83a23 = Parameter(name = 'I83a23',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rd3x5)*complexconjugate(yd2x2)',
                   texname = '\\text{I83a23}')

I83a31 = Parameter(name = 'I83a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rd1x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I83a31}')

I83a32 = Parameter(name = 'I83a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rd2x6)*complexconjugate(yd3x3)',
                   texname = '\\text{I83a32}')

I84a26 = Parameter(name = 'I84a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'yu2x2*complexconjugate(Rd6x2)',
                   texname = '\\text{I84a26}')

I84a31 = Parameter(name = 'I84a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'yu3x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I84a31}')

I84a32 = Parameter(name = 'I84a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'yu3x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I84a32}')

I85a15 = Parameter(name = 'I85a15',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rl5x1)',
                   texname = '\\text{I85a15}')

I85a26 = Parameter(name = 'I85a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rl6x2)',
                   texname = '\\text{I85a26}')

I85a31 = Parameter(name = 'I85a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rl1x3)',
                   texname = '\\text{I85a31}')

I85a34 = Parameter(name = 'I85a34',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rl4x3)',
                   texname = '\\text{I85a34}')

I86a12 = Parameter(name = 'I86a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rl2x4)*complexconjugate(ye1x1)',
                   texname = '\\text{I86a12}')

I86a23 = Parameter(name = 'I86a23',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rl3x5)*complexconjugate(ye2x2)',
                   texname = '\\text{I86a23}')

I86a31 = Parameter(name = 'I86a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rl1x6)*complexconjugate(ye3x3)',
                   texname = '\\text{I86a31}')

I86a34 = Parameter(name = 'I86a34',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rl4x6)*complexconjugate(ye3x3)',
                   texname = '\\text{I86a34}')

I87a13 = Parameter(name = 'I87a13',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rn3x1)',
                   texname = '\\text{I87a13}')

I87a22 = Parameter(name = 'I87a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rn2x2)',
                   texname = '\\text{I87a22}')

I87a31 = Parameter(name = 'I87a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Rn1x3)',
                   texname = '\\text{I87a31}')

I88a13 = Parameter(name = 'I88a13',
                   nature = 'internal',
                   type = 'complex',
                   value = 'ye1x1*complexconjugate(Rn3x1)',
                   texname = '\\text{I88a13}')

I88a22 = Parameter(name = 'I88a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'ye2x2*complexconjugate(Rn2x2)',
                   texname = '\\text{I88a22}')

I88a31 = Parameter(name = 'I88a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'ye3x3*complexconjugate(Rn1x3)',
                   texname = '\\text{I88a31}')

I89a15 = Parameter(name = 'I89a15',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Ru5x1)',
                   texname = '\\text{I89a15}')

I89a26 = Parameter(name = 'I89a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Ru6x2)',
                   texname = '\\text{I89a26}')

I89a31 = Parameter(name = 'I89a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Ru1x3)',
                   texname = '\\text{I89a31}')

I89a32 = Parameter(name = 'I89a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Ru2x3)',
                   texname = '\\text{I89a32}')

I9a15 = Parameter(name = 'I9a15',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd5x1',
                  texname = '\\text{I9a15}')

I9a26 = Parameter(name = 'I9a26',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd6x2',
                  texname = '\\text{I9a26}')

I9a31 = Parameter(name = 'I9a31',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd1x3',
                  texname = '\\text{I9a31}')

I9a32 = Parameter(name = 'I9a32',
                  nature = 'internal',
                  type = 'complex',
                  value = 'Rd2x3',
                  texname = '\\text{I9a32}')

I90a23 = Parameter(name = 'I90a23',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Ru3x5)*complexconjugate(yu2x2)',
                   texname = '\\text{I90a23}')

I90a31 = Parameter(name = 'I90a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Ru1x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I90a31}')

I90a32 = Parameter(name = 'I90a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'complexconjugate(Ru2x6)*complexconjugate(yu3x3)',
                   texname = '\\text{I90a32}')

I91a26 = Parameter(name = 'I91a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'yd2x2*complexconjugate(Ru6x2)',
                   texname = '\\text{I91a26}')

I91a31 = Parameter(name = 'I91a31',
                   nature = 'internal',
                   type = 'complex',
                   value = 'yd3x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I91a31}')

I91a32 = Parameter(name = 'I91a32',
                   nature = 'internal',
                   type = 'complex',
                   value = 'yd3x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I91a32}')

I92a11 = Parameter(name = 'I92a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I92a11}')

I92a12 = Parameter(name = 'I92a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I92a12}')

I92a21 = Parameter(name = 'I92a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I92a21}')

I92a22 = Parameter(name = 'I92a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I92a22}')

I92a55 = Parameter(name = 'I92a55',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru5x1*complexconjugate(Rd5x1)',
                   texname = '\\text{I92a55}')

I92a66 = Parameter(name = 'I92a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru6x2*complexconjugate(Rd6x2)',
                   texname = '\\text{I92a66}')

I93a11 = Parameter(name = 'I93a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn1x3*complexconjugate(Rl1x3)',
                   texname = '\\text{I93a11}')

I93a14 = Parameter(name = 'I93a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn1x3*complexconjugate(Rl4x3)',
                   texname = '\\text{I93a14}')

I93a26 = Parameter(name = 'I93a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn2x2*complexconjugate(Rl6x2)',
                   texname = '\\text{I93a26}')

I93a35 = Parameter(name = 'I93a35',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rn3x1*complexconjugate(Rl5x1)',
                   texname = '\\text{I93a35}')

I94a11 = Parameter(name = 'I94a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I94a11}')

I94a12 = Parameter(name = 'I94a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I94a12}')

I94a21 = Parameter(name = 'I94a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I94a21}')

I94a22 = Parameter(name = 'I94a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I94a22}')

I94a55 = Parameter(name = 'I94a55',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd5x1*complexconjugate(Ru5x1)',
                   texname = '\\text{I94a55}')

I94a66 = Parameter(name = 'I94a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd6x2*complexconjugate(Ru6x2)',
                   texname = '\\text{I94a66}')

I95a11 = Parameter(name = 'I95a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3*complexconjugate(Rn1x3)',
                   texname = '\\text{I95a11}')

I95a14 = Parameter(name = 'I95a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3*complexconjugate(Rn1x3)',
                   texname = '\\text{I95a14}')

I95a26 = Parameter(name = 'I95a26',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl6x2*complexconjugate(Rn2x2)',
                   texname = '\\text{I95a26}')

I95a35 = Parameter(name = 'I95a35',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl5x1*complexconjugate(Rn3x1)',
                   texname = '\\text{I95a35}')

I96a11 = Parameter(name = 'I96a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I96a11}')

I96a12 = Parameter(name = 'I96a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(Rd1x3)',
                   texname = '\\text{I96a12}')

I96a21 = Parameter(name = 'I96a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd1x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I96a21}')

I96a22 = Parameter(name = 'I96a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd2x3*complexconjugate(Rd2x3)',
                   texname = '\\text{I96a22}')

I96a55 = Parameter(name = 'I96a55',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd5x1*complexconjugate(Rd5x1)',
                   texname = '\\text{I96a55}')

I96a66 = Parameter(name = 'I96a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rd6x2*complexconjugate(Rd6x2)',
                   texname = '\\text{I96a66}')

I97a11 = Parameter(name = 'I97a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3*complexconjugate(Rl1x3)',
                   texname = '\\text{I97a11}')

I97a14 = Parameter(name = 'I97a14',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3*complexconjugate(Rl1x3)',
                   texname = '\\text{I97a14}')

I97a41 = Parameter(name = 'I97a41',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl1x3*complexconjugate(Rl4x3)',
                   texname = '\\text{I97a41}')

I97a44 = Parameter(name = 'I97a44',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl4x3*complexconjugate(Rl4x3)',
                   texname = '\\text{I97a44}')

I97a55 = Parameter(name = 'I97a55',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl5x1*complexconjugate(Rl5x1)',
                   texname = '\\text{I97a55}')

I97a66 = Parameter(name = 'I97a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Rl6x2*complexconjugate(Rl6x2)',
                   texname = '\\text{I97a66}')

I98a11 = Parameter(name = 'I98a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I98a11}')

I98a12 = Parameter(name = 'I98a12',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Ru1x3)',
                   texname = '\\text{I98a12}')

I98a21 = Parameter(name = 'I98a21',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru1x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I98a21}')

I98a22 = Parameter(name = 'I98a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru2x3*complexconjugate(Ru2x3)',
                   texname = '\\text{I98a22}')

I98a55 = Parameter(name = 'I98a55',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru5x1*complexconjugate(Ru5x1)',
                   texname = '\\text{I98a55}')

I98a66 = Parameter(name = 'I98a66',
                   nature = 'internal',
                   type = 'complex',
                   value = 'Ru6x2*complexconjugate(Ru6x2)',
                   texname = '\\text{I98a66}')

I99a11 = Parameter(name = 'I99a11',
                   nature = 'internal',
                   type = 'complex',
                   value = 'ye1x1',
                   texname = '\\text{I99a11}')

I99a22 = Parameter(name = 'I99a22',
                   nature = 'internal',
                   type = 'complex',
                   value = 'ye2x2',
                   texname = '\\text{I99a22}')

I99a33 = Parameter(name = 'I99a33',
                   nature = 'internal',
                   type = 'complex',
                   value = 'ye3x3',
                   texname = '\\text{I99a33}')

