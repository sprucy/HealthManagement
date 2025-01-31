import React, { useMemo, CSSProperties } from 'react';
import { useGetList,useTranslate } from 'react-admin';
import DollarIcon from '@mui/icons-material/AttachMoney';
import { Box, Typography } from '@mui/material';

import { CardWithIcon, CardWithTitle, HealthLineChart } from '../components';

const styles = {
    flex: { display: 'flex'},
    flexColumn: { display: 'flex', flexDirection: 'column' },
    leftCol: { flex: 1, marginRight: '0.5em' },
    rightCol: { flex: 1, marginLeft: '0.5em' },
    singleCol: { marginTop: '0.25em', marginBottom: '0.25em' },
};

const Spacer = () => <span style={{ width: '1em' }} />;
const VerticalSpacer = () => <span style={{ height: '1em' }} />;

const BMIWeightAssess = () => {
    // 确保 useGetList 总是在组件的最开始被调用
    const { data: bmiweights, total, isPending, error } = useGetList('bmiassess');
    const translate = useTranslate();
    // 计算 firstHabitId
    const bmiweight = useMemo(() => {
        return (bmiweights && bmiweights.length > 0) ? bmiweights[0] : null;
    }, [bmiweights]);

    if (error) {
        console.error('Error fetching bmi weight assess information:', error);
        return <p>ERROR: {error.message}</p>;
    }

    if (isPending) {
        return <p>Loading...</p>;
    }

    if (!bmiweights || bmiweights.length === 0) {
        return <p>No bmi weight assess data available.</p>;
    }

    const getDataset = (index: number): number[] => {
        if (bmiweight?.dataset && Array.isArray(bmiweight.dataset[index])) {
            return bmiweight.dataset[index];
        }
        return [];
    };
    
    return (
        <div>
            <div style={styles.flexColumn as CSSProperties}>
                <div style={styles.singleCol}>
                    <Box height="3em" style={{ ...styles.singleCol, display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '1em', marginBottom: '1em'}} bgcolor="info.main" color="white">
                        <Typography variant="h5" >{translate('resources.bmiassess.name')}</Typography>
                    </Box>
                </div>
                <div style={styles.flex}>
                    <HealthLineChart 
                        title = {translate('health.bmiassess.heightchart')} 
                        height = '300'
                        xdata={getDataset(0)}
                        ydata={getDataset(1)}
                    />   
                    <Spacer />
                    <HealthLineChart 
                        title = {translate('health.bmiassess.weightchart')}  
                        height = '300'
                        xdata={getDataset(0)}
                        ydata={getDataset(2)}
                    />
                    <Spacer />
                    <HealthLineChart
                        title = {translate('health.bmiassess.waistchart')}  
                        height = '300'

                        xdata={getDataset(0)}
                        ydata={getDataset(3)}
                    />
                    <Spacer />
                    <HealthLineChart 
                        title = {translate('health.bmiassess.bmichart')}   
                        height = '300'
                        xdata={getDataset(0)}
                        ydata={getDataset(4)}
                    />
                </div>

                <div style={styles.flex}>
                    <CardWithIcon
                        to="/bodyinfos"
                        icon={DollarIcon}
                        title={translate('health.bmiassess.weekweight')}
                        subtitle={`${bmiweight.assessresult[1]}Kg`}>
                    </CardWithIcon>
                    <Spacer />
                    <CardWithIcon
                        to="/bodyinfos"
                        icon={DollarIcon}
                        title={translate('health.bmiassess.weekbmi')}
                        subtitle={`${bmiweight.assessresult[3]}`} >

                    </CardWithIcon>
                    <Spacer />
                    <CardWithIcon
                        to="/bodyinfos"
                        icon={DollarIcon}
                        title={translate('health.bmiassess.weekwaist')}
                        subtitle={`${bmiweight.assessresult[2]}`} >
                    </CardWithIcon>
                
                </div>
                <VerticalSpacer />
                <div style={styles.singleCol}>
                    <CardWithTitle title={translate('resources.bmiassess.fields.assess')} content={bmiweight.assess} />
                </div>

                <div style={styles.singleCol}>
                    <CardWithTitle title={translate('resources.bmiassess.fields.risks')} content={bmiweight.risks} />
                </div>

                <div style={styles.singleCol}>
                    <CardWithTitle title={translate('resources.bmiassess.fields.intervents')} content={bmiweight.intervents} />
                </div>
            </div>
        </div>
    );
};

export default BMIWeightAssess;