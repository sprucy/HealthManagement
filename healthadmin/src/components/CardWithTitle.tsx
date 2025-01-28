import * as React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

interface Props {
    title?: string;
    content?: string;
}

// 提取通用的 CardComponent
const CardWithTitle = ({ title,content }: Props) => (
    <Card style={{ flex: '1'}}>
        <CardContent>
            <Typography variant="h5" color="info.main">{title}</Typography>
            <Typography variant="h6">{content}</Typography>
        </CardContent>
    </Card>
);

export default CardWithTitle;
