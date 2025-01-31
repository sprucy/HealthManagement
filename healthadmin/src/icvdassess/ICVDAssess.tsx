import React, { useMemo, CSSProperties } from 'react';
import { useGetList,useTranslate } from 'react-admin';
import DollarIcon from '@mui/icons-material/AttachMoney';
import { Box, Typography } from '@mui/material';

import { CardWithIcon, CardWithTitle} from '../components';

const styles = {
    flex: { display: 'flex' },
    flexColumn: { display: 'flex', flexDirection: 'column' },
    leftCol: { flex: 1, marginRight: '0.5em' },
    rightCol: { flex: 1, marginLeft: '0.5em' },
    singleCol: { marginTop: '0.25em', marginBottom: '0.25em' },
};

const Spacer = () => <span style={{ width: '1em' }} />;
const VerticalSpacer = () => <span style={{ height: '1em' }} />;

const ICVDAssess = () => {
    // 确保 useGetList 总是在组件的最开始被调用
    const { data: icvds, total, isPending, error } = useGetList('icvdassess');
    const translate = useTranslate();

    const icvd = useMemo(() => {
        return (icvds && icvds.length > 0) ? icvds[0] : null;
    }, [icvds]);

    if (error) {
        console.error('Error fetching daily habit information:', error);
        return <p>ERROR: {error.message}</p>;
    }

    if (isPending) {
        return <p>Loading...</p>;
    }

    if (!icvds || icvds.length === 0) {
        return <p>No daily icvd data available.</p>;
    }

    return (
        <div>
            <div style={styles.flexColumn as CSSProperties}>
                <div>
                    <Box height="3em" style={{ ...styles.singleCol, display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '1em', marginBottom: '1em'}} bgcolor="info.main" color="white">
                        <Typography variant="h5" >{translate('resources.icvdassess.name')}</Typography>
                    </Box>
                </div>

                <div style={styles.flex}>
                    <CardWithIcon
                        to="/smokediabetesinfos"
                        icon={DollarIcon}
                        title={translate('health.icvdassess.currisk')}
                        subtitle={`${icvd.assessresult[0]}`}
                    />
                    <Spacer />
                    <CardWithIcon
                        to="/smokediabetesinfos"
                        icon={DollarIcon}
                        title={translate('health.icvdassess.minrisk')}
                        subtitle={`${icvd.assessresult[2]}`}
                    />
                    <Spacer />
                    <CardWithIcon
                        to="/smokediabetesinfos"
                        icon={DollarIcon}
                        title={translate('health.icvdassess.avgrisk')}
                        subtitle={`${icvd.assessresult[1]}`}
                    />
                </div>
                <VerticalSpacer />
                <div style={styles.singleCol}>
                    <CardWithTitle title={translate('resources.icvdassess.fields.assess')} content={icvd.assess} />
                </div>

                <div style={styles.singleCol}>
                    <CardWithTitle title={translate('resources.icvdassess.fields.risks')} content={icvd.risks} />
                </div>

                <div style={styles.singleCol}>
                    <CardWithTitle title={translate('resources.icvdassess.fields.intervents')} content={icvd.intervents} />
                </div>
            </div>
        </div>
    );

};
export default ICVDAssess;