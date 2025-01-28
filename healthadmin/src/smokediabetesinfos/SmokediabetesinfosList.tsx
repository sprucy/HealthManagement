import { BooleanField, Datagrid, DateField, List, ReferenceField, TextField } from 'react-admin';

export const SmokediabetesinfoList = () => (
    <List>
        <Datagrid>
            <TextField source="id" />
            <ReferenceField source="user" reference="users"  link="show"/>
            <BooleanField source="smoke" />
            <DateField source="smokestart" />
            <BooleanField source="drink" />
            <DateField source="drinkstart" />
            <BooleanField source="diabetes" />
            <DateField source="diabetesstart" />
        </Datagrid>
    </List>
);

export default SmokediabetesinfoList;