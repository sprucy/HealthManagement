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

const HabitAssess = () => {
    // 确保 useGetList 总是在组件的最开始被调用
    const { data: habits, total, isPending, error } = useGetList('habitassess');
    const translate = useTranslate();
   
    const habit = useMemo(() => {
        return (habits && habits.length > 0) ? habits[0] : null;
    }, [habits]);

    if (error) {
        console.error('Error fetching daily habit information:', error);
        return <p>ERROR: {error.message}</p>;
    }

    if (isPending) {
        return <p>Loading...</p>;
    }

    if (!habits || habits.length === 0) {
        return <p>No daily habit data available.</p>;
    }
    if (habit.username==='admin'){
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
                    <div>
                        <Box height="3em" style={{ ...styles.singleCol, display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '1em', marginBottom: '1em'}} bgcolor="info.main" color="white">
                            <Typography variant="h5" >{translate('resources.habitassess.name')}</Typography>
                        </Box>
                    </div>

                    <div style={styles.flex}>
                        <CardWithIcon
                            to="/smokediabetesinfos"
                            icon={DollarIcon}
                            title={translate('resources.habitassess.fields.smokeyear')}
                            subtitle={`${habit.smokeyear}`}
                        />
                        <Spacer />
                        <CardWithIcon
                            to="/smokediabetesinfos"
                            icon={DollarIcon}
                            title={translate('resources.habitassess.fields.drinkyear')}
                            subtitle={`${habit.drinkyear}`}
                        />
                        <Spacer />
                        <CardWithIcon
                            to="/smokediabetesinfos"
                            icon={DollarIcon}
                            title={translate('resources.habitassess.fields.diabetesyear')}
                            subtitle={`${habit.diabetesyear}`}
                        />
                    </div>
                    <VerticalSpacer />
                    <div style={styles.singleCol}>
                        <CardWithTitle title={translate('resources.habitassess.fields.assess')} content={habit.assess} />
                    </div>

                    <div style={styles.singleCol}>
                        <CardWithTitle title={translate('resources.habitassess.fields.risks')} content={habit.risks} />
                    </div>

                    <div style={styles.singleCol}>
                        <CardWithTitle title={translate('resources.habitassess.fields.intervents')} content={habit.intervents} />
                    </div>
                </div>
            </div>
        );
    };
};

export default HabitAssess;