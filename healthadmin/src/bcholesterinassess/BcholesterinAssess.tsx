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

const BcholesterinAssess = () => {
    // 确保 useGetList 总是在组件的最开始被调用
    const { data: bcholesterinassess, total, isPending, error } = useGetList('bcholesterinassess');
    const translate = useTranslate();
    let datalist: string[][] = [];
    if (bcholesterinassess && bcholesterinassess.length > 0 && bcholesterinassess[0].dataset && bcholesterinassess[0].dataset[0]) {
        datalist = [...bcholesterinassess[0].dataset];
        let prefix: string='health.bcholesterinassess.';
        // 翻译数据集类别名称
        datalist[0] = datalist[0].map((item: string) => (item.includes(prefix)) ? item : translate(prefix + item)); 
    }
    const bsassess = useMemo(() => {
        return (bcholesterinassess && bcholesterinassess.length > 0) ? bcholesterinassess[0] : null;
    }, [bcholesterinassess]);

    if (error) {
        console.error('Error fetching bcholester inassess information:', error);
        return <p>ERROR: {error.message}</p>;
    }

    if (isPending) {
        return <p>Loading...</p>;
    }

    if (!bcholesterinassess || bcholesterinassess.length === 0) {
        return <p>No bmi weight assess data available.</p>;
    }

    const getBDDataset = (index: number): number[] => {
        if (bsassess?.dataset && Array.isArray(bsassess.dataset[index])) {
            return bsassess.dataset[index];
        }
        return [];
    };
   
    return (
        <div>
            <div style={styles.flexColumn as CSSProperties}>
                <div style={styles.singleCol}>
                    <Box height="3em" style={{ ...styles.singleCol, display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '1em', marginBottom: '1em'}} bgcolor="info.main" color="white">
                        <Typography variant="h5" >{translate('resources.bcholesterinassess.name')}</Typography>
                    </Box>
                </div>
                <div style={styles.flex}>
                    <HealthAreaChart 
                        title = {translate('health.bcholesterinassess.charttitle')}
                        height = '300'
                        dataset={datalist}
                    /> 
                </div>
                <div style={styles.flex}>
                    <CardWithIcon
                        to="/bodyinfos"
                        icon={DollarIcon}
                        title={translate('health.bcholesterinassess.avgtc')}
                        subtitle={`${bsassess.assessresult[0]}mmol/L`}>
                    </CardWithIcon>
                    <Spacer />
                    <CardWithIcon
                        to="/bodyinfos"
                        icon={DollarIcon}
                        title={translate('health.bcholesterinassess.avgldl')}
                        subtitle={`${bsassess.assessresult[1]}mmol/L`} >

                    </CardWithIcon>
                    <Spacer />
                    <CardWithIcon
                        to="/bodyinfos"
                        icon={DollarIcon}
                        title={translate('health.bcholesterinassess.avghdl')}
                        subtitle={`${bsassess.assessresult[2]}mmol/L`} >
                    </CardWithIcon>
                    <Spacer />
                    <CardWithIcon
                        to="/bodyinfos"
                        icon={DollarIcon}
                        title={translate('health.bcholesterinassess.avgtg')}
                        subtitle={`${bsassess.assessresult[3]}mmol/L`} >
                    </CardWithIcon>                
                </div>
                <VerticalSpacer />
                <div style={styles.singleCol}>
                    <CardWithTitle title={translate('resources.bcholesterinassess.fields.assess')} content={bsassess.assess} />
                </div>

                <div style={styles.singleCol}>
                    <CardWithTitle title={translate('resources.bcholesterinassess.fields.risks')} content={bsassess.risks} />
                </div>

                <div style={styles.singleCol}>
                    <CardWithTitle title={translate('resources.bcholesterinassess.fields.intervents')} content={bsassess.intervents} />
                </div>
            </div>
        </div>
    );

};
export default BcholesterinAssess;