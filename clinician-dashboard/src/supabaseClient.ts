import { createClient } from '@supabase/supabase-js';


const SUPABASE_URL="https://oerwudseiibkxfkdzllm.supabase.co"; 
const SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9lcnd1ZHNlaWlia3hma2R6bGxtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ2MjExNTksImV4cCI6MjA4MDE5NzE1OX0.9yELZ1B-WAnjAYk47LBD8TeE7SWdC3juEuvz_tk1BGg";

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);