%define		package	Finder
%define		php_min_version 8.2
Summary:	Symfony Finder Component
Summary(pl.UTF-8):	Komponent Symfony Finder
Name:		php-symfony-Finder
Version:	7.2.9
Release:	2
License:	MIT
Group:		Development/Languages/PHP
Source0:	https://github.com/symfony/finder/archive/v%{version}/finder-%{version}.tar.gz
# Source0-md5:	bd94128f8fe41b78f7c99654195ebe86
URL:		https://symfony.com/doc/current/components/finder.html
BuildRequires:	%{_bindir}/php
BuildRequires:	php(tokenizer)
BuildRequires:	rpmbuild(macros) >= 1.610
Requires:	php(core) >= %{php_min_version}
Requires:	php(pcre)
Requires:	php(spl)
Requires:	php-dirs >= 1.6
Obsoletes:	php-symfony2-Finder < 7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Finder Component finds files and directories via an intuitive
fluent interface.

%description -l pl.UTF-8
Komponent Finder znajduje pliki i katalogi poprzez intuicyjny
interfejs.

%prep
%setup -q -n finder-%{version}

%build
# generate classmap autoloader
php -r '
$classes = [];
$rii = new RecursiveIteratorIterator(new RecursiveDirectoryIterator("."));
foreach ($rii as $file) {
    if ($file->isDir() || $file->getExtension() !== "php") continue;
    $path = $file->getPathname();
    if (str_contains($path, "/Tests/")) continue;
    $content = file_get_contents($path);
    $tokens = token_get_all($content);
    $ns = "";
    for ($i = 0; $i < count($tokens); $i++) {
        if (is_array($tokens[$i]) && $tokens[$i][0] === T_NAMESPACE) {
            $ns = "";
            for ($j = $i+1; $j < count($tokens); $j++) {
                if (is_array($tokens[$j]) && in_array($tokens[$j][0], [T_NAME_QUALIFIED, T_STRING]))
                    $ns .= $tokens[$j][1];
                elseif ($tokens[$j] === ";") break;
            }
        }
        if (is_array($tokens[$i]) && in_array($tokens[$i][0], [T_CLASS, T_INTERFACE, T_TRAIT, T_ENUM])) {
            if ($i > 0 && is_array($tokens[$i-1]) && $tokens[$i-1][0] === T_DOUBLE_COLON) continue;
            for ($j = $i+1; $j < count($tokens); $j++) {
                if (is_array($tokens[$j]) && $tokens[$j][0] === T_STRING) {
                    $cn = $ns ? $ns . "\\\\" . $tokens[$j][1] : $tokens[$j][1];
                    $rp = substr($path, 1); // strip leading "."
                    $classes[$cn] = $rp;
                    break;
                }
            }
        }
    }
}
ksort($classes);
$f = fopen("autoload.php", "w");
fwrite($f, "<?php\nspl_autoload_register(\n    function(\$class) {\n        static \$classes = null;\n        if (\$classes === null) {\n            \$classes = array(\n");
foreach ($classes as $c => $p) {
    fwrite($f, "                " . var_export($c, true) . " => " . var_export($p, true) . ",\n");
}
fwrite($f, "            );\n        }\n        \$cn = strtolower(\$class);\n        if (isset(\$classes[\$cn])) {\n            require __DIR__ . \$classes[\$cn];\n        }\n    },\n    true,\n    false\n);\n");
fclose($f);
'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_data_dir}/Symfony/Component/%{package}
cp -a *.php */ $RPM_BUILD_ROOT%{php_data_dir}/Symfony/Component/%{package}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%dir %{php_data_dir}/Symfony/Component/Finder
%{php_data_dir}/Symfony/Component/Finder/*.php
%{php_data_dir}/Symfony/Component/Finder/Comparator
%{php_data_dir}/Symfony/Component/Finder/Exception
%{php_data_dir}/Symfony/Component/Finder/Iterator
