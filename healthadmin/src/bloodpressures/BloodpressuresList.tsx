import { Datagrid, DateField, List, NumberField, TextField, ReferenceField } from 'react-admin';

export const BloodpressureList = () => (
    <List>
        <Datagrid>
            <TextField source="id" />
            <ReferenceField source="user" reference="users"  link="show"/>
            <DateField source="measuretime" />
            <NumberField source="DBP" />
            <NumberField source="SBP" />
            <NumberField source="HR" />

        </Datagrid>
    </List>
);

export default BloodpressureList;