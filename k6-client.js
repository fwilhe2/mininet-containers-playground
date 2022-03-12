import http from 'k6/http';
import { sleep } from 'k6';

export default function () {
  http.get('http://proxy:10000');
  sleep(1);
}
