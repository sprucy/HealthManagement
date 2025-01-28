import { Datagrid, List, NumberField, TextField } from 'react-admin';

export const HealthinterventList = () => (
    <List>
        <Datagrid>
            <TextField source="id" />
            <TextField source="intervent" />
            <NumberField source="hmtype" />
        </Datagrid>
    </List>
);

export default HealthinterventList;