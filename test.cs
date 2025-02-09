namespace COSMO.Common.COSMO_DLL_Import
{
    class csAllReadWrite
    {
        #region cppAllReadWrite
        [DllImport(DLL_Import.NameOfDLL)]
        public static extern int wrapAllReadWrite(ref IntPtr hGUI, ref IntPtr hAllReadWrite);


        [DllImport(DLL_Import.NameOfDLL)]
        public static extern int wrapAllReadWrite_getCount(ref IntPtr hAllReadWrite);
        [DllImport(DLL_Import.NameOfDLL)]
        public static extern void wrapAllReadWrite_getGroup(ref IntPtr hAllReadWrite, int i, byte[] name);
        [DllImport(DLL_Import.NameOfDLL)]
        public static extern int wrapAllReadWrite_getName(ref IntPtr hAllReadWrite, int i, byte[] name);        
        [DllImport(DLL_Import.NameOfDLL)]
        public static extern int wrapAllReadWrite_Read(ref IntPtr hAllReadWrite, int i, char[] pid, char[] path);
        [DllImport(DLL_Import.NameOfDLL)]
        public static extern int wrapAllReadWrite_Write(ref IntPtr hAllReadWrite, int i, char[] pid, char[] path);
        #endregion

        IntPtr hARW = IntPtr.Zero;
        public List<(string group, string name)> datalist = new List<(string group, string name)>();

        public csAllReadWrite(csGUI gui)
        {
            IntPtr hgui = gui.getHandler();
            wrapAllReadWrite(ref hgui, ref hARW);

            getData();
        }

        ~csAllReadWrite()
        {
        }

        public int Read(int num, string pid, string path)
        {
            return wrapAllReadWrite_Read(ref hARW, num, (pid + '\0').ToCharArray(), (path + '\0').ToCharArray());
        }

        public int Write(int num, string pid, string path)
        {
            return wrapAllReadWrite_Write(ref hARW, num, (pid + '\0').ToCharArray(), (path + '\0').ToCharArray());
        }

        private void getData()
        {
            int totalCount = wrapAllReadWrite_getCount(ref hARW);
            for(int i=0; i<totalCount; i++)
            {
                byte[] groupname = new byte[DLL_Import.MaxByte];
                wrapAllReadWrite_getGroup(ref hARW, i, groupname);
                string _groupname = System.Text.Encoding.Default.GetString(groupname).Trim();
                _groupname = _groupname.Replace("\0", "");

                byte[] paramname = new byte[DLL_Import.MaxByte];
                wrapAllReadWrite_getName(ref hARW, i, paramname);
                string _paramname = System.Text.Encoding.Default.GetString(paramname).Trim();
                _paramname = _paramname.Replace("\0", "");

                datalist.Add((_groupname, _paramname));
            }
        }
    }
}