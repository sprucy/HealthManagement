import { Datagrid, List, NumberField, TextField } from 'react-admin';

export const RiskanalysesList = () => (
    <List>
        <Datagrid>
            <TextField source="id" />
            <TextField source="risk" />
            <NumberField source="hmtype" />
        </Datagrid>
    </List>
);

export default RiskanalysesList;