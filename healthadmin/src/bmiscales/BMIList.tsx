import { Datagrid, List, NumberField, TextField } from 'react-admin';

export const BMIscaleList = () => (
    <List>
        <Datagrid>
            <TextField source="id" />
            <TextField source="bmi" />
            <NumberField source="wtype" />
        </Datagrid>
    </List>
);

export default BMIscaleList;