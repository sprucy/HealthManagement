import React, { useMemo, CSSProperties } from 'react';
import { useGetList,useTranslate } from 'react-admin';
import DollarIcon from '@mui/icons-material/AttachMoney';
import { Box, Typography } from '@mui/material';

import { CardWithIcon, CardWithTitle,HealthLineChart, HealthAreaChart } from '../components';

const styles = {
    flex: { display: 'flex'},
    flexColumn: { display: 'flex', flexDirection: 'column' },
    leftCol: { flex: 1, marginRight: '0.5em' },
    rightCol: { flex: 1, marginLeft: '0.5em' },
    singleCol: { marginTop: '0.25em', marginBottom: '0.25em' },
    cardContainer: { flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' },
    chartContainer: { flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' },

};

const Spacer = () => <span style={{ width: '1em' }} />;
const VerticalSpacer = () => <span style={{ height: '1em' }} />;

const Dashboard = () => {
    // 确保 useGetList 总是在组件的最开始被调用
    const { data: bcholesterinassess, total: bcholesterinTotal, isPending: bcholesterinIsPending, error: bcholesterinError } = useGetList('bcholesterinassess');
    const { data: bloodpressureassess, total: bloodpressureTotal, isPending: bloodpressureIsPending, error: bloodpressureError } = useGetList('bloodpressureassess');
    const { data: bmiweights, total: bmiTotal, isPending: bmiIsPending, error: bmiError } = useGetList('bmiassess');
    const { data: habits, total: habitTotal, isPending: habitIsPending, error: habitError } = useGetList('habitassess');
    const { data: icvds, total: icvdsTotal, isPending: icvdsIsPending, error: icvdsError } = useGetList('icvdassess');


    const translate = useTranslate();
    


    let bsdatalist: string[][] = [];
    if (bcholesterinassess && bcholesterinassess.length > 0 && bcholesterinassess[0].dataset && bcholesterinassess[0].dataset[0]) {
        bsdatalist = [...bcholesterinassess[0].dataset];
        let prefix: string='health.bcholesterinassess.';
        // 翻译数据集类别名称
        bsdatalist[0] = bsdatalist[0].map((item: string) => (item.includes(prefix)) ? item : translate(prefix + item)); 
    }
    let bpdatalist: string[][] = [];
    if (bloodpressureassess && bloodpressureassess.length > 0 && bloodpressureassess[0].dataset && bloodpressureassess[0].dataset[0]) {
        bpdatalist = [...bloodpressureassess[0].dataset];
        let prefix: string='health.bloodpressureassess.';
        // 翻译数据集类别名称
        bpdatalist[0] = bpdatalist[0].map((item: string) => (item.includes(prefix)) ? item : translate(prefix + item)); 
    }


    const Habit = useMemo(() => {
        return (habits && habits.length > 0) ? habits[0] : null;
    }, [habits]);
    const bmiweight = useMemo(() => {
        return (bmiweights && bmiweights.length > 0) ? bmiweights[0] : null;
    }, [bmiweights]);
    const bsassess = useMemo(() => {
        return (bcholesterinassess && bcholesterinassess.length > 0) ? bcholesterinassess[0] : null;
    }, [bcholesterinassess]);
    const bpassess = useMemo(() => {
        return (bloodpressureassess && bloodpressureassess.length > 0) ? bloodpressureassess[0] : null;
    }, [bloodpressureassess]);
    const icvd = useMemo(() => {
        return (icvds && icvds.length > 0) ? icvds[0] : null;
    }, [icvds]);

    if (habitError) {
        console.error('Error fetching daily habit information:', habitError);
        return <p>ERROR: {habitError.message}</p>;
    }
    if (bmiError) {
        console.error('Error fetching bmi weight assess information:', bmiError);
        return <p>ERROR: {bmiError.message}</p>;
    }
    if (bcholesterinError) {
        console.error('Error fetching bcholesterin assess information:', bcholesterinError);
        return <p>ERROR: {bcholesterinError.message}</p>;
    }
    if (bloodpressureError) {
        console.error('Error fetching bcholesterin assess information:', bloodpressureError);
        return <p>ERROR: {bloodpressureError.message}</p>;
    }
    if (icvdsError) {
        console.error('Error fetching daily habit information:', icvdsError);
        return <p>ERROR: {icvdsError.message}</p>;
    }

    if (habitIsPending) {
        return <p>Loading...</p>;
    }    
    if (bmiIsPending) {
        return <p>Loading...</p>;
    }
    if (bcholesterinIsPending) {
        return <p>Loading...</p>;
    }
    if (bloodpressureIsPending) {
        return <p>Loading...</p>;
    }
    if (icvdsIsPending) {
        return <p>Loading...</p>;
    }

    if (!habits || habits.length === 0) {
        return <p>No daily habit data available.</p>;
    }
    if (!bmiweights || bmiweights.length === 0) {
        return <p>No bmi weight assess data available.</p>;
    }    if (!bcholesterinassess || bcholesterinassess.length === 0) {
        return <p>No bcholesterin assess data available.</p>;
    }
    if (!bloodpressureassess || bloodpressureassess.length === 0) {
        return <p>No bloodpressure assess data available.</p>;
    }
    if (!icvds || icvds.length === 0) {
        return <p>No daily icvd data available.</p>;
    }

    const getDataset = (index: number): number[] => {
        if (bmiweight?.dataset && Array.isArray(bmiweight.dataset[index])) {
            return bmiweight.dataset[index];
        }
        return [];
    };
    if (bmiweight.username==='admin'){
        return(
            <div>
                <div style={styles.singleCol}>
                    <Box height="3em" style={{ ...styles.singleCol, display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '1em', marginBottom: '1em'}} bgcolor="info.main" color="white">
                        <Typography variant="h5" >{translate('health.systemuserwarning')}</Typography>
                    </Box>

                </div>
        </div>            
        )
    }
    else{ 
        return (
            <div>
                <div style={styles.flexColumn as CSSProperties}>
                    <div style={styles.singleCol}>
                        <Box height="3em" style={{ ...styles.singleCol, display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '1em', marginBottom: '1em' }} bgcolor="info.main" color="white">
                            <Typography variant="h5">{translate('health.dashboard.title')}</Typography>
                        </Box>
                    </div>
                    <div style={styles.flex}>
                        <div style={styles.cardContainer}>
                            <CardWithIcon
                                to="/smokediabetesinfos"
                                icon={DollarIcon}
                                title={translate('resources.habitassess.fields.smokeyear')}
                                subtitle={`${Habit.smokeyear}`}
                            />
                        </div>
                        <Spacer />
                        <div style={styles.cardContainer}>
                            <CardWithIcon
                                to="/smokediabetesinfos"
                                icon={DollarIcon}
                                title={translate('resources.habitassess.fields.drinkyear')}
                                subtitle={`${Habit.drinkyear}`}
                            />
                        </div>
                        <Spacer />
                        <div style={styles.cardContainer}>
                            <CardWithIcon
                                to="/smokediabetesinfos"
                                icon={DollarIcon}
                                title={translate('resources.habitassess.fields.diabetesyear')}
                                subtitle={`${Habit.diabetesyear}`}
                            />
                        </div>
                    </div>
                    <VerticalSpacer />
                    <div style={styles.flex}>
                        <div style={styles.chartContainer}>
                            <HealthAreaChart
                                title={translate('health.bloodpressureassess.charttitle')}
                                height='300'
                                dataset={bpdatalist}
                            />
                        </div>
                        <div style={styles.chartContainer}>
                            <HealthAreaChart
                                title={translate('health.bcholesterinassess.charttitle')}
                                height='300'
                                dataset={bsdatalist}
                            />
                        </div>
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
                    <div style={styles.flex}>
                        <div style={styles.chartContainer}>
                            <HealthLineChart
                                title={translate('health.bmiassess.heightchart')}
                                height='300'
                                xdata={getDataset(0)}
                                ydata={getDataset(1)}
                            />
                        </div>
                        <Spacer />
                        <div style={styles.chartContainer}>
                            <HealthLineChart
                                title={translate('health.bmiassess.weightchart')}
                                height='300'
                                xdata={getDataset(0)}
                                ydata={getDataset(2)}
                            />
                        </div>
                        <Spacer />
                        <div style={styles.chartContainer}>
                            <HealthLineChart
                                title={translate('health.bmiassess.waistchart')}
                                height='300'
                                xdata={getDataset(0)}
                                ydata={getDataset(3)}
                            />
                        </div>
                        <Spacer />
                        <div style={styles.chartContainer}>
                            <HealthLineChart
                                title={translate('health.bmiassess.bmichart')}
                                height='300'
                                xdata={getDataset(0)}
                                ydata={getDataset(4)}
                            />
                        </div>
                    </div>

                    <VerticalSpacer />                
    
                </div>
            </div>
        );
    };
};
export default Dashboard;