use inc::Module::Install;

version '1.200';
tests 't/*.t t/*/*.t t/*/*/*.t';
test_requires 'Test::More' => '0.96';
test_requires 'Test::WWW::Mechanize::PSGI';
test_requires 'Plack';

auto_install;

WriteAll;
