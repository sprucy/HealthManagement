import { NumberField, Show, SimpleShowLayout, TextField } from 'react-admin';

export const WeightscaleShow = () => (
    <Show>
        <SimpleShowLayout>
            <TextField source="id" />
            <TextField source="sex" />
            <NumberField source="maxv" />
            <NumberField source="score" />
        </SimpleShowLayout>
    </Show>
);

export default WeightscaleShow;