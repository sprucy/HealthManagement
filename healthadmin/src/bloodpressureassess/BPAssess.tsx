import React, { useMemo, CSSProperties } from 'react';
import { useGetList,useTranslate } from 'react-admin';
import DollarIcon from '@mui/icons-material/AttachMoney';
import { Box, Typography } from '@mui/material';

import { CardWithIcon, CardWithTitle, HealthAreaChart } from '../components';

const styles = {
    flex: { display: 'flex'},
    flexColumn: { display: 'flex', flexDirection: 'column' },
    leftCol: { flex: 1, marginRight: '0.5em' },
    rightCol: { flex: 1, marginLeft: '0.5em' },
    singleCol: { marginTop: '0.25em', marginBottom: '0.25em' },
};

const Spacer = () => <span style={{ width: '1em' }} />;
const VerticalSpacer = () => <span style={{ height: '1em' }} />;

const BPAssess = () => {
    // 确保 useGetList 总是在组件的最开始被调用
    const { data: bloodpressureassess, total, isPending, error } = useGetList('bloodpressureassess');
    const translate = useTranslate();
    let datalist: string[][] = [];
    if (bloodpressureassess && bloodpressureassess.length > 0 && bloodpressureassess[0].dataset && bloodpressureassess[0].dataset[0]) {
        datalist = [...bloodpressureassess[0].dataset];
        let prefix: string='health.bloodpressureassess.';
        // 翻译数据集类别名称
        datalist[0] = datalist[0].map((item: string) => (item.includes(prefix)) ? item : translate(prefix + item)); 
    }

    const bpassess = useMemo(() => {
        return (bloodpressureassess && bloodpressureassess.length > 0) ? bloodpressureassess[0] : null;
    }, [bloodpressureassess]);

    if (error) {
        console.error('Error fetching bmi weight assess information:', error);
        return <p>ERROR: {error.message}</p>;
    }

    if (isPending) {
        return <p>Loading...</p>;
    }

    if (!bloodpressureassess || bloodpressureassess.length === 0) {
        return <p>No bmi bloodpressure assess data available.</p>;
    }
    
    
    return (
        <div>
            <div style={styles.flexColumn as CSSProperties}>
                <div style={styles.singleCol}>
                    <Box height="3em" style={{ ...styles.singleCol, display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '1em', marginBottom: '1em'}} bgcolor="info.main" color="white">
                        <Typography variant="h5" >{translate('resources.bloodpressureassess.name')}</Typography>
                    </Box>
                </div>
                <div style={styles.flex}>
                    <HealthAreaChart 
                        title = {translate('health.bloodpressureassess.charttitle')}
                        height = '300'
                        dataset={datalist}
                    />   
                </div>

                <div style={styles.flex}>
                    <CardWithIcon
                        to="/bloodpressures"
                        icon={DollarIcon}
                        title={translate('health.bloodpressureassess.avgdbp')}
                        subtitle={`${bpassess.assessresult[0]}mmol/L`}>
                    </CardWithIcon>
                    <Spacer />
                    <CardWithIcon
                        to="/bloodpressures"
                        icon={DollarIcon}
                        title={translate('health.bloodpressureassess.avgsbp')}
                        subtitle={`${bpassess.assessresult[1]}mmol/L`} >

                    </CardWithIcon>
                    <Spacer />
                    <CardWithIcon
                        to="/bloodpressures"
                        icon={DollarIcon}
                        title={translate('health.bloodpressureassess.avghr')}
                        subtitle={`${bpassess.assessresult[2]}/min`} >
                    </CardWithIcon>
                
                </div>
                <VerticalSpacer />
                <div style={styles.singleCol}>
                    <CardWithTitle title={translate('resources.bloodpressureassess.fields.assess')} content={bpassess.assess} />
                </div>

                <div style={styles.singleCol}>
                    <CardWithTitle title={translate('resources.bloodpressureassess.fields.risks')} content={bpassess.risks} />
                </div>

                <div style={styles.singleCol}>
                    <CardWithTitle title={translate('resources.bloodpressureassess.fields.intervents')} content={bpassess.intervents} />
                </div>
            </div>
        </div>
    );

};

export default BPAssess;