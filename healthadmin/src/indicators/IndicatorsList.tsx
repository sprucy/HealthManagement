import { Datagrid, List, NumberField, TextField } from 'react-admin';

export const IndicatorList = () => (
    <List>
        <Datagrid>
            <TextField source="id" />
            <TextField source="name" />
            <NumberField source="parent" />
        </Datagrid>
    </List>
);

export default IndicatorList;