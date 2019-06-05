
preliminary_voe = """<?xml version="1.0" ?>
<voe:VOEvent xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:voe="http://www.ivoa.net/xml/VOEvent/v2.0"
xsi:schemaLocation="http://www.ivoa.net/xml/VOEvent/v2.0 http://www.ivoa.net/xml/VOEvent/VOEvent-v2.0.xsd"
 version="2.0" role="test" ivorn="ivo://gwnet/LVC#MS181101ab-1-Preliminary">
    <Who>
        <Date>2018-11-01T22:34:49</Date>
        <Author>
            <contactName>LIGO Scientific Collaboration and Virgo Collaboration</contactName>
        </Author>
    </Who>
    <What>
        <Param name="internal" dataType="int" value="0">
            <Description>Indicates whether this event should be distributed to LSC/Virgo members only</Description>
        </Param>
        <Param name="Packet_Type" dataType="int" value="150">
            <Description>The Notice Type number is assigned/used within GCN, eg type=150 is an LVC_PRELIMINARY notice</Description>
        </Param>
        <Param name="Pkt_Ser_Num" dataType="string" value="1">
            <Description>A number that increments by 1 each time a new revision is issued for this event</Description>
        </Param>
        <Param name="GraceID" dataType="string" value="MS181101ab" ucd="meta.id">
            <Description>Identifier in GraceDB</Description>
        </Param>
        <Param name="AlertType" dataType="string" value="Preliminary" ucd="meta.version">
            <Description>VOEvent alert type</Description>
        </Param>
        <Param name="HardwareInj" dataType="int" value="0" ucd="meta.number">
            <Description>Indicates that this event is a hardware injection if 1, no if 0</Description>
        </Param>
        <Param name="OpenAlert" dataType="int" value="1" ucd="meta.number">
            <Description>Indicates that this event is an open alert if 1, no if 0</Description>
        </Param>
        <Param name="EventPage" dataType="string" value="https://example.org/superevents/MS181101ab/view/" ucd="meta.ref.url">
            <Description>Web page for evolving status of this GW candidate</Description>
        </Param>
        <Param name="Instruments" dataType="string" value="H1,L1,V1" ucd="meta.code">
            <Description>List of instruments used in analysis to identify this event</Description>
        </Param>
        <Param name="FAR" dataType="float" value="9.11069936486e-14" ucd="arith.rate;stat.falsealarm" unit="Hz">
            <Description>False alarm rate for GW candidates with this strength or greater</Description>
        </Param>
        <Param name="Group" dataType="string" value="CBC" ucd="meta.code">
            <Description>Data analysis working group</Description>
        </Param>
        <Param name="Pipeline" dataType="string" value="gstlal" ucd="meta.code">
            <Description>Low-latency data analysis pipeline</Description>
        </Param>
        <Param name="Search" dataType="string" value="MDC" ucd="meta.code">
            <Description>Specific low-latency search</Description>
        </Param>
        <Group type="GW_SKYMAP" name="bayestar">
            <Param name="skymap_fits" dataType="string" value="https://emfollow.docs.ligo.org/userguide/_static/bayestar.fits.gz" ucd="meta.ref.url">
                <Description>Sky Map FITS</Description>
            </Param>
        </Group>
        <Group type="Classification">
            <Description>Source classification: binary neutron star (BNS), neutron star-black hole (NSBH), binary black hole (BBH), MassGap, or terrestrial (noise)</Description>
            <Param name="BNS" dataType="float" value="0.95" ucd="stat.probability">
                <Description>Probability that the source is a binary neutron star merger (both objects lighter than 3 solar masses)</Description>
            </Param>
            <Param name="NSBH" dataType="float" value="0.01" ucd="stat.probability">
                <Description>Probability that the source is a neutron star-black hole merger (primary heavier than 5 solar masses, secondary lighter than 3 solar masses)</Description>
            </Param>
            <Param name="BBH" dataType="float" value="0.03" ucd="stat.probability">
                <Description>Probability that the source is a binary black hole merger (both objects heavier than 5 solar masses)</Description>
            </Param>
            <Param name="MassGap" dataType="float" value="0.0" ucd="stat.probability">
                <Description>Probability that the source has at least one object between 3 and 5 solar masses</Description>
            </Param>
            <Param name="Terrestrial" dataType="float" value="0.01" ucd="stat.probability">
                <Description>Probability that the source is terrestrial (i.e., a background noise fluctuation or a glitch)</Description>
            </Param>
        </Group>
        <Group type="Properties">
            <Description>Qualitative properties of the source, conditioned on the assumption that the signal is an astrophysical compact binary merger</Description>
            <Param name="HasNS" dataType="float" value="0.95" ucd="stat.probability">
                <Description>Probability that at least one object in the binary has a mass that is less than 2.83 solar masses</Description>
            </Param>
            <Param name="HasRemnant" dataType="float" value="0.91" ucd="stat.probability">
                <Description>Probability that a nonzero mass was ejected outside the central remnant object</Description>
            </Param>
        </Group>
    </What>
    <WhereWhen>
        <ObsDataLocation>
            <ObservatoryLocation id="LIGO Virgo"/>
            <ObservationLocation>
                <AstroCoordSystem id="UTC-FK5-GEO"/>
                <AstroCoords coord_system_id="UTC-FK5-GEO">
                    <Time>
                        <TimeInstant>
                            <ISOTime>2018-11-01T22:22:46.654437</ISOTime>
                        </TimeInstant>
                    </Time>
                </AstroCoords>
            </ObservationLocation>
        </ObsDataLocation>
    </WhereWhen>
    <How>
        <Description>Candidate gravitational wave event identified by low-latency analysis</Description>
        <Description>H1: LIGO Hanford 4 km gravitational wave detector</Description>
        <Description>L1: LIGO Livingston 4 km gravitational wave detector</Description>
        <Description>V1: Virgo 3 km gravitational wave detector</Description>
    </How>
    <Description>Report of a candidate gravitational wave event</Description>
</voe:VOEvent>
"""

initial_voe = """<?xml version="1.0" ?>
<voe:VOEvent xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:voe="http://www.ivoa.net/xml/VOEvent/v2.0"
xsi:schemaLocation="http://www.ivoa.net/xml/VOEvent/v2.0 http://www.ivoa.net/xml/VOEvent/VOEvent-v2.0.xsd"
 version="2.0" role="test" ivorn="ivo://gwnet/LVC#MS181101ab-2-Initial">
    <Who>
        <Date>2018-11-01T22:36:25</Date>
        <Author>
            <contactName>LIGO Scientific Collaboration and Virgo Collaboration</contactName>
        </Author>
    </Who>
    <What>
        <Param name="internal" dataType="int" value="0">
            <Description>Indicates whether this event should be distributed to LSC/Virgo members only</Description>
        </Param>
        <Param name="Packet_Type" dataType="int" value="151">
            <Description>The Notice Type number is assigned/used within GCN, eg type=151 is an LVC_INITIAL notice</Description>
        </Param>
        <Param name="Pkt_Ser_Num" dataType="string" value="2">
            <Description>A number that increments by 1 each time a new revision is issued for this event</Description>
        </Param>
        <Param name="GraceID" dataType="string" value="MS181101ab" ucd="meta.id">
            <Description>Identifier in GraceDB</Description>
        </Param>
        <Param name="AlertType" dataType="string" value="Initial" ucd="meta.version">
            <Description>VOEvent alert type</Description>
        </Param>
        <Param name="HardwareInj" dataType="int" value="0" ucd="meta.number">
            <Description>Indicates that this event is a hardware injection if 1, no if 0</Description>
        </Param>
        <Param name="OpenAlert" dataType="int" value="1" ucd="meta.number">
            <Description>Indicates that this event is an open alert if 1, no if 0</Description>
        </Param>
        <Param name="EventPage" dataType="string" value="https://example.org/superevents/MS181101ab/view/" ucd="meta.ref.url">
            <Description>Web page for evolving status of this GW candidate</Description>
        </Param>
        <Param name="Instruments" dataType="string" value="H1,L1,V1" ucd="meta.code">
            <Description>List of instruments used in analysis to identify this event</Description>
        </Param>
        <Param name="FAR" dataType="float" value="9.11069936486e-14" ucd="arith.rate;stat.falsealarm" unit="Hz">
            <Description>False alarm rate for GW candidates with this strength or greater</Description>
        </Param>
        <Param name="Group" dataType="string" value="CBC" ucd="meta.code">
            <Description>Data analysis working group</Description>
        </Param>
        <Param name="Pipeline" dataType="string" value="gstlal" ucd="meta.code">
            <Description>Low-latency data analysis pipeline</Description>
        </Param>
        <Param name="Search" dataType="string" value="MDC" ucd="meta.code">
            <Description>Specific low-latency search</Description>
        </Param>
        <Group type="GW_SKYMAP" name="bayestar">
            <Param name="skymap_fits" dataType="string" value="https://emfollow.docs.ligo.org/userguide/_static/bayestar.fits.gz" ucd="meta.ref.url">
                <Description>Sky Map FITS</Description>
            </Param>
        </Group>
        <Group type="Classification">
            <Description>Source classification: binary neutron star (BNS), neutron star-black hole (NSBH), binary black hole (BBH), MassGap, or terrestrial (noise)</Description>
            <Param name="BNS" dataType="float" value="0.95" ucd="stat.probability">
                <Description>Probability that the source is a binary neutron star merger (both objects lighter than 3 solar masses)</Description>
            </Param>
            <Param name="NSBH" dataType="float" value="0.01" ucd="stat.probability">
                <Description>Probability that the source is a neutron star-black hole merger (primary heavier than 5 solar masses, secondary lighter than 3 solar masses)</Description>
            </Param>
            <Param name="BBH" dataType="float" value="0.03" ucd="stat.probability">
                <Description>Probability that the source is a binary black hole merger (both objects heavier than 5 solar masses)</Description>
            </Param>
            <Param name="MassGap" dataType="float" value="0.0" ucd="stat.probability">
                <Description>Probability that the source has at least one object between 3 and 5 solar masses</Description>
            </Param>
            <Param name="Terrestrial" dataType="float" value="0.01" ucd="stat.probability">
                <Description>Probability that the source is terrestrial (i.e., a background noise fluctuation or a glitch)</Description>
            </Param>
        </Group>
        <Group type="Properties">
            <Description>Qualitative properties of the source, conditioned on the assumption that the signal is an astrophysical compact binary merger</Description>
            <Param name="HasNS" dataType="float" value="0.95" ucd="stat.probability">
                <Description>Probability that at least one object in the binary has a mass that is less than 2.83 solar masses</Description>
            </Param>
            <Param name="HasRemnant" dataType="float" value="0.91" ucd="stat.probability">
                <Description>Probability that a nonzero mass was ejected outside the central remnant object</Description>
            </Param>
        </Group>
    </What>
    <WhereWhen>
        <ObsDataLocation>
            <ObservatoryLocation id="LIGO Virgo"/>
            <ObservationLocation>
                <AstroCoordSystem id="UTC-FK5-GEO"/>
                <AstroCoords coord_system_id="UTC-FK5-GEO">
                    <Time>
                        <TimeInstant>
                            <ISOTime>2018-11-01T22:22:46.654437</ISOTime>
                        </TimeInstant>
                    </Time>
                </AstroCoords>
            </ObservationLocation>
        </ObsDataLocation>
    </WhereWhen>
    <How>
        <Description>Candidate gravitational wave event identified by low-latency analysis</Description>
        <Description>H1: LIGO Hanford 4 km gravitational wave detector</Description>
        <Description>L1: LIGO Livingston 4 km gravitational wave detector</Description>
        <Description>V1: Virgo 3 km gravitational wave detector</Description>
    </How>
    <Citations>
        <EventIVORN cite="supersedes">ivo://gwnet/LVC#MS181101ab-1-Preliminary</EventIVORN>
        <Description>Updated localization is now available</Description>
    </Citations>
    <Description>Report of a candidate gravitational wave event</Description>
</voe:VOEvent>
"""

update_voe = """<?xml version="1.0" ?>
<voe:VOEvent xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:voe="http://www.ivoa.net/xml/VOEvent/v2.0"
xsi:schemaLocation="http://www.ivoa.net/xml/VOEvent/v2.0 http://www.ivoa.net/xml/VOEvent/VOEvent-v2.0.xsd"
 version="2.0" role="test" ivorn="ivo://gwnet/LVC#MS181101ab-3-Update">
    <Who>
        <Date>2018-11-01T22:36:25</Date>
        <Author>
            <contactName>LIGO Scientific Collaboration and Virgo Collaboration</contactName>
        </Author>
    </Who>
    <What>
        <Param name="internal" dataType="int" value="0">
            <Description>Indicates whether this event should be distributed to LSC/Virgo members only</Description>
        </Param>
        <Param name="Packet_Type" dataType="int" value="152">
            <Description>The Notice Type number is assigned/used within GCN, eg type=152 is an LVC_UPDATE notice</Description>
        </Param>
        <Param name="Pkt_Ser_Num" dataType="string" value="3">
            <Description>A number that increments by 1 each time a new revision is issued for this event</Description>
        </Param>
        <Param name="GraceID" dataType="string" value="MS181101ab" ucd="meta.id">
            <Description>Identifier in GraceDB</Description>
        </Param>
        <Param name="AlertType" dataType="string" value="Update" ucd="meta.version">
            <Description>VOEvent alert type</Description>
        </Param>
        <Param name="HardwareInj" dataType="int" value="0" ucd="meta.number">
            <Description>Indicates that this event is a hardware injection if 1, no if 0</Description>
        </Param>
        <Param name="OpenAlert" dataType="int" value="1" ucd="meta.number">
            <Description>Indicates that this event is an open alert if 1, no if 0</Description>
        </Param>
        <Param name="EventPage" dataType="string" value="https://example.org/superevents/MS181101ab/view/" ucd="meta.ref.url">
            <Description>Web page for evolving status of this GW candidate</Description>
        </Param>
        <Param name="Instruments" dataType="string" value="H1,L1,V1" ucd="meta.code">
            <Description>List of instruments used in analysis to identify this event</Description>
        </Param>
        <Param name="FAR" dataType="float" value="9.11069936486e-14" ucd="arith.rate;stat.falsealarm" unit="Hz">
            <Description>False alarm rate for GW candidates with this strength or greater</Description>
        </Param>
        <Param name="Group" dataType="string" value="CBC" ucd="meta.code">
            <Description>Data analysis working group</Description>
        </Param>
        <Param name="Pipeline" dataType="string" value="gstlal" ucd="meta.code">
            <Description>Low-latency data analysis pipeline</Description>
        </Param>
        <Param name="Search" dataType="string" value="MDC" ucd="meta.code">
            <Description>Specific low-latency search</Description>
        </Param>
        <Group type="GW_SKYMAP" name="bayestar">
            <Param name="skymap_fits" dataType="string" value="https://emfollow.docs.ligo.org/userguide/_static/bayestar.fits.gz" ucd="meta.ref.url">
                <Description>Sky Map FITS</Description>
            </Param>
        </Group>
        <Group type="Classification">
            <Description>Source classification: binary neutron star (BNS), neutron star-black hole (NSBH), binary black hole (BBH), MassGap, or terrestrial (noise)</Description>
            <Param name="BNS" dataType="float" value="0.95" ucd="stat.probability">
                <Description>Probability that the source is a binary neutron star merger (both objects lighter than 3 solar masses)</Description>
            </Param>
            <Param name="NSBH" dataType="float" value="0.01" ucd="stat.probability">
                <Description>Probability that the source is a neutron star-black hole merger (primary heavier than 5 solar masses, secondary lighter than 3 solar masses)</Description>
            </Param>
            <Param name="BBH" dataType="float" value="0.03" ucd="stat.probability">
                <Description>Probability that the source is a binary black hole merger (both objects heavier than 5 solar masses)</Description>
            </Param>
            <Param name="MassGap" dataType="float" value="0.0" ucd="stat.probability">
                <Description>Probability that the source has at least one object between 3 and 5 solar masses</Description>
            </Param>
            <Param name="Terrestrial" dataType="float" value="0.01" ucd="stat.probability">
                <Description>Probability that the source is terrestrial (i.e., a background noise fluctuation or a glitch)</Description>
            </Param>
        </Group>
        <Group type="Properties">
            <Description>Qualitative properties of the source, conditioned on the assumption that the signal is an astrophysical compact binary merger</Description>
            <Param name="HasNS" dataType="float" value="0.95" ucd="stat.probability">
                <Description>Probability that at least one object in the binary has a mass that is less than 2.83 solar masses</Description>
            </Param>
            <Param name="HasRemnant" dataType="float" value="0.91" ucd="stat.probability">
                <Description>Probability that a nonzero mass was ejected outside the central remnant object</Description>
            </Param>
        </Group>
    </What>
    <WhereWhen>
        <ObsDataLocation>
            <ObservatoryLocation id="LIGO Virgo"/>
            <ObservationLocation>
                <AstroCoordSystem id="UTC-FK5-GEO"/>
                <AstroCoords coord_system_id="UTC-FK5-GEO">
                    <Time>
                        <TimeInstant>
                            <ISOTime>2018-11-01T22:22:46.654437</ISOTime>
                        </TimeInstant>
                    </Time>
                </AstroCoords>
            </ObservationLocation>
        </ObsDataLocation>
    </WhereWhen>
    <How>
        <Description>Candidate gravitational wave event identified by low-latency analysis</Description>
        <Description>H1: LIGO Hanford 4 km gravitational wave detector</Description>
        <Description>L1: LIGO Livingston 4 km gravitational wave detector</Description>
        <Description>V1: Virgo 3 km gravitational wave detector</Description>
    </How>
    <Citations>
        <EventIVORN cite="supersedes">ivo://gwnet/LVC#MS181101ab-1-Preliminary</EventIVORN>
        <EventIVORN cite="supersedes">ivo://gwnet/LVC#MS181101ab-2-Initial</EventIVORN>
        <Description>Updated localization is now available</Description>
    </Citations>
    <Description>Report of a candidate gravitational wave event</Description>
</voe:VOEvent>
"""

retraction_voe = """<?xml version="1.0" ?>
<voe:VOEvent xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:voe="http://www.ivoa.net/xml/VOEvent/v2.0"
xsi:schemaLocation="http://www.ivoa.net/xml/VOEvent/v2.0 http://www.ivoa.net/xml/VOEvent/VOEvent-v2.0.xsd"
 version="2.0" role="test" ivorn="ivo://gwnet/LVC#MS181101ab-4-Retraction">
    <Who>
        <Date>2018-11-01T23:36:23</Date>
        <Author>
            <contactName>LIGO Scientific Collaboration and Virgo Collaboration</contactName>
        </Author>
    </Who>
    <What>
        <Param name="internal" dataType="int" value="0">
            <Description>Indicates whether this event should be distributed to LSC/Virgo members only</Description>
        </Param>
        <Param name="Packet_Type" dataType="int" value="164">
            <Description>The Notice Type number is assigned/used within GCN, eg type=164 is an LVC_RETRACTION notice</Description>
        </Param>
        <Param name="Pkt_Ser_Num" dataType="string" value="4">
            <Description>A number that increments by 1 each time a new revision is issued for this event</Description>
        </Param>
        <Param name="GraceID" dataType="string" value="MS181101ab" ucd="meta.id">
            <Description>Identifier in GraceDB</Description>
        </Param>
        <Param name="AlertType" dataType="string" value="Retraction" ucd="meta.version">
            <Description>VOEvent alert type</Description>
        </Param>
        <Param name="HardwareInj" dataType="int" value="0" ucd="meta.number">
            <Description>Indicates that this event is a hardware injection if 1, no if 0</Description>
        </Param>
        <Param name="OpenAlert" dataType="int" value="1" ucd="meta.number">
            <Description>Indicates that this event is an open alert if 1, no if 0</Description>
        </Param>
        <Param name="EventPage" dataType="string" value="https://example.org/superevents/MS181101ab/view/" ucd="meta.ref.url">
            <Description>Web page for evolving status of this GW candidate</Description>
        </Param>
    </What>
    <WhereWhen>
        <ObsDataLocation>
            <ObservatoryLocation id="LIGO Virgo"/>
            <ObservationLocation>
                <AstroCoordSystem id="UTC-FK5-GEO"/>
                <AstroCoords coord_system_id="UTC-FK5-GEO">
                    <Time>
                        <TimeInstant>
                            <ISOTime>2018-11-01T22:22:46.654437</ISOTime>
                        </TimeInstant>
                    </Time>
                </AstroCoords>
            </ObservationLocation>
        </ObsDataLocation>
    </WhereWhen>
    <Citations>
        <EventIVORN cite="retraction">ivo://gwnet/LVC#MS181101ab-1-Preliminary</EventIVORN>
        <EventIVORN cite="retraction">ivo://gwnet/LVC#MS181101ab-2-Initial</EventIVORN>
        <EventIVORN cite="retraction">ivo://gwnet/LVC#MS181101ab-3-Update</EventIVORN>
        <Description>Determined to not be a viable GW event candidate</Description>
    </Citations>
</voe:VOEvent>
"""

minicat = """#PGC   Name   RA   Dec   Type   App_Mag   Maj_Diam_a   err_Maj_Diam   Min_Diam_b   err_Min_Diam   b/a   err_b/a   PA   Abs_Mag   Dist   err_Dist   err_App_Mag   err_Abs_Mag  
2 UGC12889 0.00047 47.27450 3.1 13.31 1.546 0.498 1.314 NaN 0.85 0.100 NaN -21.05 72.458 10.869 0.61 0.61 
4 PGC000004 0.00096 23.08764 5.0 15.39 0.851 0.078 0.186 NaN 0.219 0.015 NaN -18.68 63.264 13.918 0.39 0.40 
6 PGC000006 0.00058 15.88165 -1.0 15.23 0.457 0.169 0.324 NaN 0.708 0.082 NaN -19.46 84.181 18.520 0.34 0.35 
7 PGC000007 0.00122 -0.08326 -3.2 15.54 0.575 0.093 0.467 NaN 0.813 0.056 NaN -19.46 97.347 21.416 0.33 0.34 
10 PGC000010 0.00217 -0.04057 -3.2 15.56 0.562 0.078 0.446 NaN 0.794 0.037 NaN -19.46 98.250 21.615 0.29 0.31 
12 PGC000012 0.00240 -6.37390 1.1 14.05 1.045 0.336 0.199 NaN 0.19 0.022 NaN -20.79 92.153 13.823 0.36 0.37 
13 PGC000013 0.00370 33.13420 NaN 15.41 0.675 0.217 0.587 NaN 0.87 0.102 NaN -18.94 72.722 10.908 0.40 0.41 
16 PGC000016 0.00314 -5.15871 1.2 14.60 0.630 0.203 0.328 NaN 0.52 0.061 NaN -19.93 79.278 11.892 0.29 0.30 
18 PGC000018 0.00360 46.96508 NaN 14.25 0.869 0.280 0.791 NaN 0.91 0.107 NaN -20.25 77.306 11.596 0.31 0.32 
31 PGC000031 0.00657 -47.01893 0 14.67 0.740 0.238 0.466 NaN 0.63 0.074 NaN -19.91 85.389 12.808 0.34 0.35 
38 UGC12893 0.00792 17.22027 8.4 15.14 1.148 0.159 1.023 NaN 0.891 0.062 NaN -15.97 16.222 3.569 0.38 0.39 
43 ESO293-027 0.00819 -40.48439 3.9 13.27 1.443 0.465 0.375 NaN 0.26 0.031 NaN -19.87 43.069 6.460 0.28 0.29 
49 PGC000049 0.00931 22.77842 NaN 16.85 0.316 0.102 0.288 NaN 0.91 0.107 NaN -17.87 85.389 18.786 1.01 1.01 
53 UGC12895 0.01064 20.05896 7.6 16.46 0.617 0.099 0.457 NaN 0.741 0.051 NaN -18.48 94.819 20.860 0.49 0.50 
55 UGC12898 0.01039 33.60095 5.9 15.90 0.776 0.072 0.234 NaN 0.302 0.021 NaN -18.33 68.333 15.033 0.35 0.36 
65 ESO193-009 0.01479 -47.35683 -0.9 15.03 0.850 0.274 0.221 NaN 0.26 0.031 NaN -19.51 81.236 12.185 0.21 0.22 
70 UGC12900 0.01557 20.33792 5.8 13.82 1.778 0.123 0.258 NaN 0.145 0.010 NaN -21.14 95.583 21.028 0.29 0.31 
73 ESO349-017 0.01627 -33.61189 5.1 14.36 0.707 0.228 0.601 NaN 0.85 0.100 NaN -20.56 95.722 14.358 0.28 0.29 
76 UGC12901 0.01636 28.91169 3.0 13.99 1.094 0.352 0.416 NaN 0.38 0.045 NaN -21.01 98.278 14.742 0.33 0.34 
81 NGC7802 0.01677 6.24195 -2.0 14.35 0.811 0.261 0.406 NaN 0.50 0.059 NaN -20.06 74.750 11.213 0.32 0.33 
89 PGC000089 0.02039 13.14406 4.9 14.84 0.741 0.085 0.295 NaN 0.398 0.028 NaN -19.64 76.486 16.827 0.07 0.12 
92 PGC000092 0.02084 13.11290 5.5 15.66 0.513 0.083 0.186 NaN 0.363 0.025 NaN -18.87 78.278 17.221 0.19 0.21 
94 UGC12905 0.03358 80.64171 6.1 NaN 1.072 0.148 0.129 NaN 0.120 0.017 NaN NaN 60.833 13.383 NaN NaN 
101 NGC7803 0.02221 13.11128 0.0 13.56 0.500 0.161 0.295 NaN 0.59 0.069 NaN -20.88 76.528 11.479 0.11 0.13 
102 IC5376 0.02216 34.52572 2.0 13.78 1.443 0.465 0.245 NaN 0.17 0.020 NaN -20.57 72.472 10.871 0.32 0.33 
108 PGC000108 0.02386 13.11310 9.0 14.64 0.281 0.091 0.239 NaN 0.85 0.100 NaN -19.75 75.000 11.250 0.10 0.12 
109 NGC7805 0.02410 31.43378 -1.9 13.90 0.870 0.280 0.722 NaN 0.83 0.098 NaN -20.40 71.236 10.685 0.10 0.12 
110 UGC12910 0.02450 5.38890 9.0 NaN 0.912 0.210 0.912 NaN 1.000 0.138 NaN NaN 54.931 12.085 NaN NaN 
112 NGC7806 0.02503 31.44192 4.1 13.63 0.850 0.274 0.663 NaN 0.78 0.092 NaN -20.60 68.722 10.308 0.16 0.17 
"""
