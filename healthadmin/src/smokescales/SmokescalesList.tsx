import { BooleanField, Datagrid, List, NumberField, TextField } from 'react-admin';

export const SmokescaleList = () => (
    <List>
        <Datagrid>
            <TextField source="id" />
            <TextField source="sex" />
            <BooleanField source="smoke" />
            <NumberField source="score" />
        </Datagrid>
    </List>
);

export default SmokescaleList;